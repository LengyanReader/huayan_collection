// ═══ DATA ═══
var GRAPH = __GRAPH__;
var GAP = __GAP__;
var DATA=GRAPH, map=null, selectedId=null, selectedId2=null, searchQuery="";
var tl={canvas:null,ctx:null,W:0,H:0,ox:0,oy:0,scale:1,minX:100,maxX:2060,rows:[],hitRects:[],drag:false,lastX:0};
var nodeMap={}; DATA.nodes.forEach(function(n){nodeMap[n.id]=n;});
