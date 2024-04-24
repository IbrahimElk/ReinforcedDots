function restart() {
	var i,j,x;
	score[0]=0;
	score[1]=0;
	for (i=0;i<=m;i++) {
		x=2*i*nn+1
		for (j=0;j<n;j++) {
			document.images[x+2*j].src=n3.src;
			hedge[i][j]=0;
		}
	}
	for (i=0;i<m;i++) {
		x=(2*i+1)*nn
		for (j=0;j<=n;j++) {
			document.images[x+2*j].src=n3.src;
			vedge[i][j]=0;
		}
	}
	for (i=0;i<m;i++) {
		x=(2*i+1)*nn+1
		for (j=0;j<n;j++) {
			document.images[x+2*j].src=n3.src;
			box[i][j]=0;
		}
	}
	if (player!=1) makemove();
}

// function hmove(i,j) {     //horizontal move by user
// 	if (hedge[i][j]<1) {
// 		sethedge(i,j);
// 		if (score[0]+score[1]==m*n) {
// 			alert("Game over.\r Score: Red = "+score[0]+",  Blue = "+score[1])
// 		} else if (player==0) makemove();
// 	}
// }

// function vmove(i,j) {     //vertical move by user
// 	if (vedge[i][j]<1) {
// 		setvedge(i,j);
// 		if (score[0]+score[1]==m*n) {
// 			alert("Game over.\r Score: Red = "+score[0]+",  Blue = "+score[1])
// 		} else if (player==0) makemove();
// 	}
// }

function sethedge(x,y) {      //Sets horizontal edge
	hedge[x][y]=1;
	if (x>0) box[x-1][y]++;
	if (x<m) box[x][y]++;
	document.images[2*x*nn+2*y+1].src=n2.src;
	checkh(x,y)
	player=1-player;
}

function setvedge(x,y) {      //Sets vertical edge
 	vedge[x][y]=1;
	if (y>0) box[x][y-1]++;
	if (y<n) box[x][y]++;
	document.images[(2*x+1)*nn+2*y].src=n2.src;
	checkv(x,y)
	player=1-player;
}


function makemove() {
	// take all box which would be finished within one edge, 
	// which don't cause the creation of other capturable boxes. 
	takesafe3s();
	if (sides3()) { // check if there are other boxes to caputure with already 3 edges, but would create other capturable boxes. 
		if (sides01()) { // if there is a random safe edge that you can capture
			takeall3s();	// first take all boxes that you could capture
			takeedge(zz,x,y); // then take the random safe edge. 
		} else { // if there are no other random safe edge that you can capture. 
			sac(u,v) // capture all boxes but leave a double left. 
		}	
		if (score[0]+score[1]==m*n) {
			alert("Game over.\r Score: Red = "+score[0]+",  Blue = "+score[1])
		}
	} else if (sides01()) takeedge(zz,x,y);
	else if (singleton()) takeedge(zz,x,y);
	else if (doubleton()) takeedge(zz,x,y);
	else makeanymove();
}

function takeedge(zz,x,y) {    //Set hedge if zz=1 and vedge if zz=2.
	if (zz>1) setvedge(x,y);
	else sethedge(x,y);
}

function takesafe3s() {     //Take all singleton and doubleton 3's.
	for (var i=0;i<m;i++) {
		for (var j=0;j<n;j++) {
			if (box[i][j]==3) {
				if (vedge[i][j]<1) {
					// box[i][j-1]!=2: This constraint checks if the box to the left 
					// of the current box (i, j) does not have a value of 2 
					// (which means it is not a doubleton). 
					// If this condition is true, it allows setting the vertical edge 
					// to the left of the current box (i, j).
					// in other words, you dont create a 3-edge chain to the left of this box. 
					if (j==0 || box[i][j-1]!=2) setvedge(i,j);  
				} else if (hedge[i][j]<1) {
					if (i==0 || box[i-1][j]!=2) sethedge(i,j);
				} else if (vedge[i][j+1]<1) {
					if (j==n-1 || box[i][j+1]!=2) setvedge(i,j+1);
				} else {
					if (i==m-1 || box[i+1][j]!=2) sethedge(i+1,j);
				}
			}
		}
	}
}

function sides3() {     //Returns true and u,v if there is a box(u,v)=3.
	for (var i=0;i<m;i++) {
		for (var j=0;j<n;j++) {
			if (box[i][j]==3) {
				u=i;
				v=j;
				return true;
			}
		}
	}
	return false;
}

function takeall3s() {
	while (sides3()) takebox(u,v);
}

function sides01() {     //Returns true and zz,x,y if there is a safe edge(x,y).
	if (Math.random()<.5) zz=1; else zz=2;  //zz=1 if horizontal, zz=2 if vertical
	var i=Math.floor(m*Math.random());
	var j=Math.floor(n*Math.random());
	if (zz==1) {
		if (randhedge(i,j)) return true;
		else {
			zz=2;
			if (randvedge(i,j)) return true;
		}
	} else {
		if (randvedge(i,j)) return true;
		else {
			zz=1;
			if (randhedge(i,j)) return true;
		}
	}
	return false;
}

function safehedge(i,j) {     //Returns true if (i,j) is a safe hedge
	if (hedge[i][j]<1) {
		if (i==0) {
			if (box[i][j]<2) return true
		} else if (i==m) {
			if (box[i-1][j]<2) return true
		}
		else if (box[i][j]<2 && box[i-1][j]<2) return true;
	}
	return false
}

function safevedge(i,j) {
	if (vedge[i][j]<1) {
		if (j==0) {
			if (box[i][j]<2) return true
		} else if (j==n) {
			if (box[i][j-1]<2) return true
		}
		else if (box[i][j]<2 && box[i][j-1]<2) return true;
	}
	return false
}

function randhedge(i,j) {
	x=i;
	y=j;
	do {
		if (safehedge(x,y)) return true;
		else {
			y++;
			if (y==n) {
				y=0;
				x++;
				if (x>m) x=0;
			}
		}
	} while (x!=i || y!=j);
	return false
}

function randvedge(i,j) {
	x=i;
	y=j;
	do {
		if (safevedge(x,y)) return true;
		else {
			y++;
			if (y>n) {
				y=0;
				x++;
				if (x==m) x=0;
			}
		}
	} while (x!=i || y!=j);
	return false
}
	
function singleton() {     //Returns true and zz,x,y if edge(x,y) gives exactly
	var numb;              //1 square away
	for (var i=0;i<m;i++) {
		for (var j=0;j<n;j++) {
			if (box[i][j]==2) {
				numb=0;
				if (hedge[i][j]<1) {
					if (i<1 || box[i-1][j]<2) numb++;
				}
				zz=2;
				if (vedge[i][j]<1) {
					if (j<1 || box[i][j-1]<2) numb++;
					if (numb>1) {
						x=i;
						y=j;
						return true;
					}
				}
				if (vedge[i][j+1]<1) {
					if (j+1==n || box[i][j+1]<2) numb++;
					if (numb>1) {
						x=i;
						y=j+1;
						return true;
					}
				}
				zz=1;
				if (hedge[i+1][j]<1) {
					if (i+1==m || box[i+1][j]<2) numb++;
					if (numb>1) {
						x=i+1;
						y=j;
						return true;
					}
				}
			}
		}
	}
	return false;
}

function doubleton() {     //Returns true and zz,x,y if edge(x,y) gives away 
	zz=2;                  //exactly 2 squares
	for (i=0;i<m;i++) {
		for (j=0;j<n-1;j++) {
			if (box[i][j]==2 && box[i][j+1]==2 && vedge[i][j+1]<1) {
				if (ldub(i,j) && rdub(i,j+1)) {
					x=i;
					y=j+1;
					return true;
				}
			}
		}
	}
	zz=1;
	for (j=0;j<n;j++) {
		for (i=0;i<m-1;i++) {
			if (box[i][j]==2 && box[i+1][j]==2 && hedge[i+1][j]<1) {
				if (udub(i,j) && ddub(i+1,j)) {
					x=i+1;
					y=j;
					return true;
				}
			}
		}
	}
	return false
}

function ldub(i,j) {      //Given box(i,j)=2 and vedge(i,j+1)=0, returns true
	if (vedge[i][j]<1) {      //if the other free edge leads to a box<2
		if (j<1 || box[i][j-1]<2) return true; 
	} else if (hedge[i][j]<1) {
		if (i<1 || box[i-1][j]<2) return true;
	} else if (i==m-1|| box[i+1][j]<2) {
		return true
	}
	return false
}

function rdub(i,j) {
	if (vedge[i][j+1]<1) {
		if (j+1==n || box[i][j+1]<2) return true;
	} else if (hedge[i][j]<1) {
		if (i<1 || box[i-1][j]<2) return true;
	} else if (i+1==m || box[i+1][j]<2) {
		return true
	}
	return false
}
				
function udub(i,j) {
	if (hedge[i][j]<1) {
		if (i<1 || box[i-1][j]<2) return true;
	} else if (vedge[i][j]<1) {
		if (j<1 || box[i][j-1]<2) return true;
	} else if (j==n-1 || box[i][j+1]<2) {
		return true
	}
	return false
}

function ddub(i,j) {
	if (hedge[i+1][j]<1) {
		if (i==m-1 || box[i+1][j]<2) return true;
	} else if (vedge[i][j]<1) {
		if (j<1 || box[i][j-1]<2) return true;
	} else if (j==n-1 || box[i][j+1]<2) {
		return true
	}
	return false
}


function sac(i,j) {     //sacrifices two squares if there are still 3's
    count=0;
	loop=false;
	incount(0,i,j);
	if (!loop) takeallbut(i,j);
	if (count+score[0]+score[1]==m*n) {
		takeall3s()
	} else {
		if (loop) {
			count=count-2;
		}
		outcount(0,i,j);
		i=m;
		j=n
	}
}

function incount(k,i,j) {  //enter with box[i][j]=3 and k=0
    count++;               //returns count = number in chain starting at i,j
	//k=1,2,3,4 means skip left,up,right,down.

	// k!= 1 dus choose left side of box in order to explore chain.  
	if (k!=1 && vedge[i][j]<1) {     
		// ibr: ik denk j>0 wegens de representatie die ze gebruiken. 
		// aangezien de matrix van vertical edges en de matrix van horizontal edges, van dimensies verschillen 
		// aangezien er meerdere verticale edges zijn in een rij dan dat er horizontale edges zijn in een rij van dots and boxes. 
		// anyway, not certain, maar kdenk niet zo belangerijk om het te verstaan.
		if (j>0) {
			// als vedge[i][j] < 1 => dus er is geen vertical line in dot (i,j). (oftwel van dot (i,j) naar (i+1,j))
			// en k!=1, wat het ook initieel is, want initieel k = 0 
			// dus stel box
			//     *	*	*
			// 
			// 	   * 	*	*
			// met volgende indexen: 
			// 		(i,	 j-1)	(i,	 j)	(i,	 j+1)
			// 
			//		(i+1,j-1)	(i+1,j)	(i+1,j+1)
			// 
			// bv. met de volgende configuratie: 
			//     *----*---*
			// 	   |		|
			// 	   *----*---*
			// 
			// dan is vedge(i,j) = 1 want er is een edge van (i,j) naar (i+1,j).
			// de vraag is dan, is box(i,j-1) oftewel de box met als linkerboven dot (i,j-1), 
			// bevat die box meer dan 2 edges? 
			// in ons geval is de box (i,j-1) oftwel de box {(i, j-1), (i, j), (i+1, j), (i+1, j-1)}
			// bevat 3 edges. dus if statement is true. 
			// dan increasen we de count, 
			// want we willen het aantal capturable boxen vinden als we starten vanuit (i,j) (aantal boxen in de chain)
			// loop is true, want zoals je ziet in de schema hierboven , vormt de configuratie een loop. 
			// we roepen niet nogmaals inCount, want de chain is closed en we weten nu hoeveel boxes in de chain er zittne
			// namelijk 2.

			if (box[i][j-1]>2) { // als de linker box ook al 3 edges bevat, 
				count++;
				loop=true;
			} 
			// bv. met de volgende configuratie: 
			//     *----*---*
			// 	   			|
			// 	   *----*---*
			// 
			// dan als hoeven we niet naar rechts te kijken, vandaar, we roepen de functie op
			// nogmaals op, maar nu startend van positie (i, j-1). 
			// (aangezien dit javascript is, 
			// hoef je de lokale variabelen niet meegeven in de argumet, 
			// zoals count, omdat ze globaal gedeclareerd zijn....)
			// maar je werkt dus verder met wat je als had bij count. 
			// k=3 dus skip right.

			// of de volgende configuraties zijn ook mogelijk hier:  (andere dan deze niet denk ik)
			//     *----*---*
			// 	   |		|
			// 	   *	*---*
			// 
			//     * 	*---*
			// 	   |		|
			// 	   *----*---*

			else if (box[i][j-1]>1) {
				incount(3,i,j-1);
			}
		}
	// k!= 2 dus choose up side of box in order to explore chain. 
	} else if (k!=2 && hedge[i][j]<1) {
		// k!=2 oftewel, skip up.
		// bv. met de volgende configuratie:  
		// 
		//     *----*
		// 	   |    |
		//     * 	*
		// 	   |    |
		// 	   *----*
		// 
		// met volgende indexen: 
		// 		(i-1, 	j)	(i-1,	j+1) 
		//		(i,		j)	(i,		j+1) 
		// 		(i+1, 	j)	(i+1,	j+1) 
		// 
		// waarbij de box {(i, j), (i, j+1), (i+1, j+1), (i+1, j)} al 3 edges bevat. (meer dan 2)
		// en de box met linkerboven hoek (i-1,j) al meer dan 2 edges bevat, 3 edges dus. 
		// zoals in de diagram heirboven. 
		// dan count++ (want er is 1 box extra box dat gecaptured kan worden in de chain, de bovenste box)
		// en het is ook een loop (closed chain) 
		// analoog aan eerste if statement. 
		if (i>0) {
			if (box[i-1][j]>2) {
				count++;
				loop=true
			} 
			// indien de bovenste box niet 3 edges bevat maar minder, dus 2 edges 
			// dan is het een half open chain, en dus call je functie recursief, die dus count++ doet in het begin
			// en nogmaals verder zoekt achter andere boxes die horen bij deze chain. 
			else if (box[i-1][j]>1) {
				//     *----*
				// 	        |
				//     * 	*
				// 	   |    |
				// 	   *----*	

				//     *----*
				// 	   |     
				//     * 	*
				// 	   |    |
				// 	   *----*	

				//     * 	*
				// 	   |    | 
				//     * 	*
				// 	   |    |
				// 	   *----*	

				incount(4,i-1,j);
			}
		}
	
		
	// k!= 3 dus choose right side of box in order to explore chain. 
	} else if (k!=3 && vedge[i][j+1]<1) {
		if (j<n-1) {
			// bv. met de volgende configuratie:  


			// bv. met de volgende configuratie: 
			//     *----*---*
			// 	   |		|
			// 	   *----*---*

			// met volgende indexen: 
			// 		(i,	 j)	(i,	 j+1)	(i,	 j+2)
			// 
			//		(i+1,j)	(i+1,j+1)	(i+1,j+2)
			// 
			
			if (box[i][j+1]>2) {
				count++;
				loop=true
			} 
			
			else if (box[i][j+1]>1) {
				//     *----*---*
				// 	   |		|
				// 	   *----*	*
				
				//     *----*	*
				// 	   |		|
				// 	   *----*---*

				//     *----*---*
				// 	   |		
				// 	   *----*---*

				incount(1,i,j+1);
			}
		}


	// k!= 4 dus choose down side of box in order to explore chain.  
	} else if (k!=4 && hedge[i+1][j]<1) {
		if (i<m-1) {
			// bv. met de volgende configuratie:  
			// 
			//     *----*
			// 	   |    |
			//     * 	*
			// 	   |    |
			// 	   *----*
			// 
			// met volgende indexen: 
			// 		(i, 	j)	(i,		j+1) 
			//		(i+1,	j)	(i+1,	j+1) 
			// 		(i+2, 	j)	(i+2,	j+1) 
			// 
			// waarbij de box {(i, j), (i, j+1), (i+1, j+1), (i+1, j)} al 3 edges bevat. (meer dan 2)
			// en de box met linkerboven hoek (i+1,j) al meer dan 2 edges bevat, 3 edges dus. 
			// zoals in de diagram heirboven. 
			// dan count++ (want er is 1 box extra box dat gecaptured kan worden in de chain, de onderste box)
			// en het is ook een loop (closed chain) 
			// analoog aan tweede if statement. 
			
			if (box[i+1][j]>2) {
				count++;
				loop=true
			} 


				//     *----*
				// 	   |    |
				//     * 	*
				// 	        |
				// 	   *----*	

				//     *----*
				// 	   |    | 
				//     * 	*
				// 	   |    
				// 	   *----*	

				//     *----*
				// 	   |    | 
				//     * 	*
				// 	   |    |
				// 	   *	*	


			else if (box[i+1][j]>1) {
				incount(2,i+1,j);
			}
		}
	}
}

function takeallbut(x,y) {
	while (sides3not(x,y)) {
		takebox(u,v);
	}
}
	
function sides3not(x,y) {
	for (var i=0;i<m;i++) {
		for (var j=0;j<n;j++) {
			if (box[i][j]==3) {
				if (i!=x || j!=y) {
					u=i;
					v=j;
					return true;
				}
			}
		}
	}
	return false
}

function takebox(i,j) {
	if (hedge[i][j]<1) sethedge(i,j);
	else if (vedge[i][j]<1) setvedge(i,j);
	else if (hedge[i+1][j]<1) sethedge(i+1,j);
	else setvedge(i,j+1);
}

function outcount(k,i,j) {     //Takes all but count-2 squares and exits
	if (count>0) {
		if (k!=1 && vedge[i][j]<1) {
			if (count!=2) setvedge(i,j);
			count--;
			outcount(3,i,j-1)
		} else if (k!=2 && hedge[i][j]<1) {
			if (count!=2) sethedge(i,j);
			count--;
			outcount(4,i-1,j)
		} else if (k!=3 && vedge[i][j+1]<1) {
			if (count!=2) setvedge(i,j+1);
			count--;
			outcount(1,i,j+1)
		} else if (k!=4 && hedge[i+1][j]<1) {
			if (count!=2) sethedge(i+1,j);
			count--;
			outcount(2,i+1,j)
		}
	}
}

function makeanymove() {
	x=-1;
	for (i=0;i<=m;i++) {
		for (j=0;j<n;j++) {
			if (hedge[i][j]<1) {
				x=i;
				y=j;
				i=m+1;
				j=n
			}
		}
	}
	if (x<0) {
		for (i=0;i<m;i++) {
			for (j=0;j<=n;j++) {
				if (vedge[i][j]<1) {
					x=i;
					y=j;
					i=m;
					j=n+1;
				}
			}
		}
		setvedge(x,y);
	} else {
		sethedge(x,y);
	}
	if (player==0) makemove();
}

function checkh(x,y) {     //check if hedge move scores any points
	var hit=0;
	if (x>0) {
		if (box[x-1][y]==4) {
			var uu=x-1;
			document.images[(2*uu+1)*nn+2*y+1].src=flag[player];
			score[player]++;
			hit=1;
		}
	}
	if (x<m) {
		if (box[x][y]==4) {
			document.images[(2*x+1)*nn+2*y+1].src=flag[player];
			score[player]++;
			hit=1;
		}
	}
	if (hit>0) player=1-player;
}

function checkv(x,y) {
	var hit=0;
	if (y>0) {
		if (box[x][y-1]==4) {
			var vv=y-1;
			document.images[(2*x+1)*nn+2*vv+1].src=flag[player];
			score[player]++;
			hit=1;
		}
	}
	if (y<n) {
		if (box[x][y]==4) {
			document.images[(2*x+1)*nn+2*y+1].src=flag[player];
			score[player]++;
			hit=1;
		}
	}
	if (hit>0) player=1-player;
}

var m;
var n;

n0 = new Image();
n1 = new Image();
n2 = new Image();
n3 = new Image();

n0.src = "red.gif";
n1.src = "blue.gif";
n2.src = "black.gif";
n3.src = "blank.gif";

var flag = [n0.src,n1.src];
var player=1;
var score=[0,0];
var hedge=[];
var vedge=[];
var box=[];
var nn,x,y,zz,count,loop,u,v;

function getInput() {
	do {
		m=window.prompt("Enter number of rows between 3 and 9.","4");
	} while (m<3 || m>9);
	do {
		n=window.prompt("Enter number of columns between 3 and 9.","4");
	} while (n<3 || n>9);
	for (var i=0;i<=m;i++) {
		hedge[i]=[];
		for (var j=0;j<n;j++) hedge[i][j]=0;
	}
	for (i=0;i<m;i++) {
		vedge[i]=[];
		for (j=0;j<=n;j++) vedge[i][j]=0;
	}
	for (i=0;i<m;i++) {
		box[i]=[];
		for (j=0;j<n;j++) box[i][j]=0;
	}
	nn=2*n+1;
}
getInput();

// get input from user, and execute vmove or hmove accordingly. 
// then the ai agent will execute since it is called in one of those functions. 


// this could be usefull for us as a benchmark alongside random agent. 

// THIS IS THE AGENT :
// function makemoveAgent() {
// 	takesafe3s();
// 	if (sides3()) {
// 		if (sides01()) {
// 			takeall3s();
// 			takeedge(zz,x,y);
// 		} else {
// 			sac(u,v)
// 		}	
// 		if (score[0]+score[1]==m*n) {
// 			alert("Game over.\r Score: Red = "+score[0]+",  Blue = "+score[1])
// 		}
// 	} 
// 	else if (sides01()) takeedge(zz,x,y);
// 	else if (singleton()) takeedge(zz,x,y);
// 	else if (doubleton()) takeedge(zz,x,y);
// 	else makeanymove();
// }


