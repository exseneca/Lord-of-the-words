//var tomovelist = document.getElementsByClassName("tomove")

let tomovelist = document.getElementsByClassName("tomove")

for(let i=0; i<tomovelist.length; i++){

let tomove = tomovelist[i];


tomove.onmousedown = function(event){
    event.preventDefault();
    // (1) prepare to moving: make absolute and on top by z-index
    tomove.style.position = 'absolute';
    tomove.style.zIndex = 1001;

   
    mydiv = document.getElementById("mydiv");
    //mydiv.style.position = 'absolute';
    
    leftbound = mydiv.getBoundingClientRect().left;
    topbound = mydiv.getBoundingClientRect().top;

    originalleft = tomove.getBoundingClientRect().left;
    originaltop = tomove.getBoundingClientRect().top;

   let shiftX = event.clientX - tomove.getBoundingClientRect().left;
   let shiftY = event.clientY - tomove.getBoundingClientRect().top;


    // var originalleft = tomove.style.left;
    // var originaltop = tomove.style.top;
    // move it out of any current parents directly into body
    // to make it positioned relative to the body 
    // document.body.append(tomove);


   
   
    // centers the div at (pageX, pageY) coordinates
    function moveAt(pageX, pageY) {
        tomove.style.left = Math.max(leftbound,pageX - shiftX) + 'px';
        tomove.style.top =  Math.max(topbound,pageY - shiftY) + 'px';
    }

    /// move our abosolutely positioned ball uner the pointer

    moveAt(event.pageX, event.pageY);

    let currentDroppable = null;
    function onMouseMove(event) {
        moveAt(event.pageX, event.pageY);

        tomove.hidden = true;
        let elemBelow = document.elementFromPoint(event.clientX, event.clientY);
        tomove.hidden = false; 

        if(!elemBelow) return;

        let droppableBelow = elemBelow.closest('.droppable');

        if (currentDroppable != droppableBelow){
            // we're flying in or out:
            // note: both elements can be null 
            // currentDropbbale = null if we were not over a droppale before this event
            // droppableBelow = null if we are not over a droppable now. 
            if (currentDroppable) {
                // the logic to process flying out of the droppable
                leaveDroppable(currentDroppable);
            } 
        }
        currentDroppable = droppableBelow;
        if (currentDroppable){
            enterDroppable(currentDroppable);
        }
    }

    function enterDroppable(currentDroppable){
        let droppableId = currentDroppable.id;
        let topspacer = document.getElementById("topspacer");
        topspacer.innerText = "You are over: " + droppableId;
    };

    function leaveDroppable(currentDropbbale){
        let topspacer = document.getElementById("topspacer");
        topspacer.innerText = "";
    }


    // (2) move the div on mousemove
    tomove.addEventListener('mousemove', onMouseMove);

    // (3) drop the div, remove unneeded handlers
    this.onmouseup = function(event) {
        tomove.removeEventListener('mousemove', onMouseMove);
        tomove.onmouseout = null;
        //tomove.style.left = originalleft;
        //tomove.style.top = originaltop;
        tomove.style.zIndex = 1000;

    };

  
   
  
    //tomove.addEventListener("onmouseup", cleanupfunction)    

    tomove.addEventListener("ondragstart", function() {
        return false;
      });
    
   

    
};

//tomove.addEventListener("onmousedown", mouse_move)

//};

};
// next, we need to add the events to multiple tiles and allow behaviour for multiple fields.
