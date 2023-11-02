document.querySelectorAll('.dropdown-context-menu').forEach( element => {
    element.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        const contextMenu = document.querySelector(element.getAttribute('data-option'));
        contextMenu.classList.add('show')
        if (document.body.clientHeight < contextMenu.clientHeight + e.screenY ){
            contextMenu.style.top = e.clientY - (contextMenu.clientHeight) +'px';
        } else {
            contextMenu.style.top = e.clientY - 5 + 'px';
        }
        contextMenu.style.left = e.clientX -5 + 'px';
        document.body.appendChild(contextMenu);

    });
})

document.querySelectorAll('.selection-element').forEach( element => {

    element.addEventListener('click', function(e) {
        if (element.classList.contains('selected'))
            return element.classList.remove('selected') 
        document.querySelectorAll(element.getAttribute('data-selection')).forEach( el => el.classList.remove('selected'))
        element.classList.add('selected')
    });
});

document.querySelector('.context-menu').addEventListener('mouseleave', (e) => {

    e.fromElement.classList.remove('show')
})

document.querySelectorAll('.folder').forEach( element => {

    element.addEventListener('click', function(e) {
        
        
    });
});

