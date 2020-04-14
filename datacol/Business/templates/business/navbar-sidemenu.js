document.addEventListener('DOMContentLoaded', () =>{
            document.getElementById('slide-open').onclick = openSlideMenu;
            document.getElementById('slide-close').onclick = closeSlideMenu;
            document.getElementById('main-main').onclick=closeSlideMenu;


        function openSlideMenu() {
            document.getElementById('side-menu').style.width = '250px';
            document.getElementById('main-main').style.marginLeft = '250px';
        }
        function closeSlideMenu() {
            document.getElementById('side-menu').style.width = 0;
            document.getElementById('main-main').style.marginLeft = 0;
        }

});