//var tomovelist = document.getElementsByClassName("tomove")




document.onmousedown = function(event){
    event.preventDefault();
    // (1) prepare to moving: make absolute and on top by z-index
    // we need to get the rack number from the class
    

    if(event.target.classList.contains('showhide')){
        let coverNumber = event.target.id.slice(-1)
        let rackCover = document.getElementById('rackcover' + coverNumber)
        if(rackCover.classList.contains('hidden')){
            rackCover.classList.remove('hidden');
            event.target.innerText = 'Show Rack'
        } else {
            event.target.innerText = 'Hide Rack'
            rackCover.classList.add('hidden');
        }
        
    }

    if(!(event.target.parentNode.classList.contains('tilecontainer'))) return;

    let  tomove = event.target.parentNode.parentNode;
    
    if(tomove.classList.contains('locked')) return;



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
    
    };

    function leaveDroppable(currentDropbbale){
        currentDroppbale = null;
    }


    // (2) move the div on mousemove
    document.addEventListener('mousemove', onMouseMove);

    // (3) drop the div, remove unneeded handlers
    this.onmouseup = async function(event) {
        document.removeEventListener('mousemove', onMouseMove);
        document.onmouseout = null;
        document.onmouseup = null;
        //tomove.style.left = originalleft;
        //tomove.style.top = originaltop;
        if(currentDroppable){
            tomove.style.left = currentDroppable.getBoundingClientRect().left;
            tomove.style.top = currentDroppable.getBoundingClientRect().top;
            tomove.classList.add('locked'); // we need this right now because if we don't lock and we move. We keep placing the same tile all over the board
            let lettertoadd = tomove.childNodes[1].childNodes[1].innerText;
            let squareid = currentDroppable.id;
            let containingdiv  = tomove.childNodes[1]
            let rackclass = containingdiv.childNodes[1].id 
            let response = await fetch('/placetile', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify({letter:lettertoadd,squareid:squareid, rackclass:rackclass})
            });
            
            let responseText = response.body;

            
           
        } else {
            tomove.style.left = originalleft;
            tomove.style.top = originaltop;
        }
        
        tomove.style.zIndex = 1000;

    };

  
   
  
    //tomove.addEventListener("onmouseup", cleanupfunction)    

    tomove.addEventListener("ondragstart", function() {
        return false;
      });
    
   

    
};

//tomove.addEventListener("onmousedown", mouse_move)

//};


// next, we need to add the events to multiple tiles and allow behaviour for multiple fields.
