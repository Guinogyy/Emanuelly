// JavaScript for scroll reveal animations and mobile menu

document.addEventListener('DOMContentLoaded', () => {
    // Scroll Reveal Logic
    const revealElements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');

    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const revealPoint = 150; // Distance from bottom to trigger

        revealElements.forEach(el => {
            const revealTop = el.getBoundingClientRect().top;

            if (revealTop < windowHeight - revealPoint) {
                el.classList.add('active');
            }
        });
    };

    // Initial check in case elements are already in view
    revealOnScroll();

    // Listen for scroll events
    window.addEventListener('scroll', revealOnScroll);

    // Mobile Menu Toggle (Basic implementation)
    const mobileMenuBtn = document.querySelector('nav button');
    const navLinks = document.querySelector('nav .hidden.md\\:flex');
    const ctaBtn = document.querySelector('nav a[href="#contact"]');

    // Create a mobile menu container if it doesn't exist
    let mobileMenu = document.createElement('div');
    mobileMenu.className = 'fixed inset-0 bg-black/95 z-40 hidden flex-col items-center justify-center space-y-8 text-2xl font-bold transition-opacity duration-300 opacity-0';

    // Clone links for mobile
    const links = document.querySelectorAll('nav .hidden.md\\:flex a');
    links.forEach(link => {
        const clone = link.cloneNode(true);
        clone.classList.remove('transition-colors', 'duration-300');
        clone.classList.add('text-white', 'hover:text-gold');
        clone.addEventListener('click', () => toggleMobileMenu());
        mobileMenu.appendChild(clone);
    });

    const ctaClone = ctaBtn.cloneNode(true);
    ctaClone.classList.remove('hidden', 'md:inline-block', 'py-2', 'px-6', 'text-sm');
    ctaClone.classList.add('mt-8', 'py-4', 'px-10', 'text-xl');
    ctaClone.addEventListener('click', () => toggleMobileMenu());
    mobileMenu.appendChild(ctaClone);

    document.body.appendChild(mobileMenu);

    let isMobileMenuOpen = false;

    const toggleMobileMenu = () => {
        isMobileMenuOpen = !isMobileMenuOpen;
        if (isMobileMenuOpen) {
            mobileMenu.classList.remove('hidden');
            // Small delay to allow display:block to apply before changing opacity
            setTimeout(() => {
                mobileMenu.classList.remove('opacity-0');
            }, 10);
            document.body.style.overflow = 'hidden'; // Prevent scrolling

            // Change icon to X
            mobileMenuBtn.innerHTML = `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>`;
        } else {
            mobileMenu.classList.add('opacity-0');
            setTimeout(() => {
                mobileMenu.classList.add('hidden');
            }, 300); // Match duration
            document.body.style.overflow = ''; // Restore scrolling

            // Restore hamburger icon
            mobileMenuBtn.innerHTML = `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>`;
        }
    };

    mobileMenuBtn.addEventListener('click', toggleMobileMenu);
});