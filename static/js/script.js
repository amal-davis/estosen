document.addEventListener('DOMContentLoaded', function () {
    const header = document.querySelector("header");
    const menu = document.querySelector('#menu-icon');
    const navlist = document.querySelector('.navlist');
    const shopLink = document.querySelector('.shop-link');
    const dropdownContent = document.querySelector('.dropdown-content');

    window.addEventListener("scroll", function () {
        header.classList.toggle("sticky", window.scrollY > 80);
    });

    menu.onclick = () => {
        menu.classList.toggle('bx-x');
        navlist.classList.toggle('open');
        dropdownContent.classList.remove('open');
    };

    // Toggle the dropdown on small screens with a single click on the arrow icon
    shopLink.addEventListener('click', function (e) {
        e.preventDefault();
        dropdownContent.classList.toggle('open');
    });

    // Close the dropdown when clicking outside
    document.addEventListener('click', function (e) {
        if (!shopLink.contains(e.target) && !dropdownContent.contains(e.target)) {
            dropdownContent.classList.remove('open');
        }
    });

    // Close the dropdown when clicking on the arrow icon again
    shopLink.addEventListener('click', function (e) {
        if (dropdownContent.classList.contains('open') && shopLink.contains(e.target)) {
            dropdownContent.classList.remove('open');
        } else {
            dropdownContent.classList.add('open');
        }
    });

    window.onscroll = () => {
        menu.classList.remove('bx-x');
        navlist.classList.remove('open');
        dropdownContent.classList.remove('open');
    };

    const sr = ScrollReveal({
        origin: 'top',
        distance: '85px',
        duration: 2500,
        reset: true
    });

    sr.reveal('.home-text', { delay: 300 });
    sr.reveal('.home-img', { delay: 400 });
});
