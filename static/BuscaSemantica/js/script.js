document.querySelectorAll('.inner-addon').forEach( addon => {
    addon.querySelector('i').addEventListener('click', ()=> addon.querySelector('input').dispatchEvent(new KeyboardEvent('keyup',{keyCode: 13})))
})
