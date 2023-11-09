window.FolderTree = new FolderTree( document.querySelector('#folder-tree'), document.querySelector('#folder-filter'));
window.FileForm = new FileForm( document.querySelector('#form_document'));

// document.querySelectorAll('.dropdown-context-menu').forEach( element => {
//     element.addEventListener('contextmenu', function(e) {
//         e.preventDefault();
//         const id = e.currentTarget.parentElement.getAttribute('data-id')
//         document.querySelector('#add_edit_folder input[name="id"]').value = id;
//         document.querySelector('#delete_folder input[name="id"]').value = id;
//         document.querySelector('#add_edit_folder input[name="name"]').value = e.currentTarget.querySelector(`.folder[data-id="${id}"]`).textContent;
//         if (e.currentTarget.parentElement.getAttribute('data-parent') != "None")
//             document.querySelector('#add_edit_folder select[name="id_parent_dir"]').value = e.currentTarget.parentElement.getAttribute('data-parent');
//         const contextMenu = document.querySelector(element.getAttribute('data-option'));
//         contextMenu.classList.add('show')
//         if (document.body.clientHeight < contextMenu.clientHeight + e.screenY ){
//             contextMenu.style.top = e.clientY - (contextMenu.clientHeight) +'px';
//         } else {
//             contextMenu.style.top = e.clientY - 5 + 'px';
//         }
//         contextMenu.style.left = e.clientX -5 + 'px';
//         document.body.appendChild(contextMenu);

//     });
// })

// document.querySelectorAll('.selection-element').forEach( element => {

//     element.addEventListener('click', function(e) {
//         if (element.classList.contains('selected'))
//             return element.classList.remove('selected') 
//         document.querySelectorAll(element.getAttribute('data-selection')).forEach( el => el.classList.remove('selected'))
//         element.classList.add('selected')
//     });
// });
// const context = document.querySelector('.context-menu')
// if (context){
//     context.addEventListener('mouseleave', (e) => {
    
//         e.fromElement.classList.remove('show')
//     })
// }

// function addEditFolder(ev){
//     folder = new Folder(ev.srcElement, document.querySelector('#folder-tree'))
//     folder.addSaveFolder();
//     return false
// }

// function deleteFolder(){
//     folder = new Folder(document.querySelector('#delete_folder'), document.querySelector('#folder-tree'))
//     folder.deleteFolder();
//     return false
// }

// const editFolder = document.querySelector('#add_edit_folder');
// if (editFolder){
//     editFolder.addEventListener('shown.bs.modal', (ev) => {
//         ev.srcElement.querySelector('#folder-action-title').textContent = ev.relatedTarget.getAttribute('data-action-title');
//         if (ev.relatedTarget.getAttribute('data-action') != 'edit'){
//             document.querySelector('#add_edit_folder input[name="id"]').value = '';
//             document.querySelector('#add_edit_folder input[name="name"]').value = '';
//             document.querySelector('#add_edit_folder select[name="id_parent_dir"]').value = '';
//         }
//     })
// }


