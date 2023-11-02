document.querySelectorAll('.dropdown-context-menu').forEach( element => {
    element.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        document.querySelector('#add_edit_folder input[name="id"]').value = e.currentTarget.parentElement.getAttribute('data-id');
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

function addEditFolder(ev){
    folder = new Folder(ev.srcElement, document.querySelector('#folder-tree'))
    folder.addSaveFolder().then( data => {
        console.log(data)
    });
    return false
}

document.querySelector('#add_edit_folder').addEventListener('shown.bs.modal', (ev) => {
    ev.srcElement.querySelector('#folder-action-title').textContent = ev.relatedTarget.getAttribute('data-action-title');
})

document.querySelectorAll('.folder').forEach( element => {
    element['folder-filter'] = document.querySelector('#filter-folder')
    element.addEventListener('click', function(e) {
        const folder = document.createElement('span');
        folder.className = 'badge rounded-pill text-bg-secondary text-white mx-1';
        folder.setAttribute('role','button');
        folder.setAttribute('data-id', element.getAttribute('data-id'));
        folder.textContent = element.textContent;
        folder.innerHTML += '<i class="bi bi-x"></i>'
        folder.addEventListener('click', () => folder.remove())
        element['folder-filter'].appendChild(folder);
    });
});

