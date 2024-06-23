function toggleMenu() {
    var menu = document.getElementById('menu');
    if (menu.classList.contains('show-menu')) {
        menu.classList.remove('show-menu');
    } else {
        menu.classList.add('show-menu');
    }
}
