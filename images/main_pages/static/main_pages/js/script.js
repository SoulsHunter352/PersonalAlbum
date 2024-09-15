
let sidebar = document.querySelector('.sidebar');
let button = document.querySelector(".button-sidebar-wrapper");
button.addEventListener("click", () => {
    sidebar.classList.toggle('active');
    button.classList.toggle('active');
})

let wrapper = document.querySelector('#modal_wrapper');
let form = document.querySelector('#confirm_delete');

function show_modal(slug)
{
    form.action = slug;
    wrapper.style.display = 'block';
}

function close_modal()
{
    wrapper.style.display = 'none';
}
