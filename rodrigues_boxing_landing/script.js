document.addEventListener('DOMContentLoaded', () => {

    // --- Mobile Menu Toggle ---
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });

    // Close mobile menu on link click
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    });

    // --- Smooth Scrolling for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Adjust for fixed header
                    behavior: 'smooth'
                });
            }
        });
    });

    // --- Scroll Reveal Animations ---
    const revealElements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');

    const revealOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            }
            entry.target.classList.add('active');
            observer.unobserve(entry.target);
        });
    }, revealOptions);

    revealElements.forEach(el => {
        revealOnScroll.observe(el);
    });

    // --- Header Scroll Effect ---
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('py-2');
            header.classList.remove('py-4');
        } else {
            header.classList.add('py-4');
            header.classList.remove('py-2');
        }
    });

    // --- FAQ Accordion Functionality ---
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const btn = item.querySelector('.faq-btn');
        const content = item.querySelector('.faq-content');
        const icon = item.querySelector('.faq-icon');

        btn.addEventListener('click', () => {
            const isOpen = item.classList.contains('active-faq');

            // Close all other FAQs (optional, if you want only one open at a time)
            faqItems.forEach(otherItem => {
                otherItem.classList.remove('active-faq');
                otherItem.querySelector('.faq-content').style.maxHeight = null;
                otherItem.querySelector('.faq-icon').classList.remove('rotate-180');
                otherItem.classList.remove('border-gold');
            });

            // Toggle current FAQ
            if (!isOpen) {
                item.classList.add('active-faq');
                item.classList.add('border-gold');
                icon.classList.add('rotate-180');
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    });

    // --- Dynamic Punch Animation for Logo ---
    const logoContainer = document.querySelector('.hero-logo-container');
    const logoImg = document.querySelector('.logo-float');

    if (logoContainer && logoImg) {
        logoContainer.addEventListener('mousemove', (e) => {
            const rect = logoContainer.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            // Subtle rotation based on mouse position
            logoImg.style.transform = `perspective(1000px) rotateY(${x / 10}deg) rotateX(${-y / 10}deg) scale(1.05)`;
        });

        logoContainer.addEventListener('mouseleave', () => {
            // Reset to default floating animation
            logoImg.style.transform = '';
        });
    }
});

// --- Map Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    // REDFIT - Parque São Jorge coordinates
    const lat = -23.525656;
    const lng = -46.565451;

    // Initialize the map if the container exists
    const mapContainer = document.getElementById('map');
    if (mapContainer && typeof L !== 'undefined') {
        const map = L.map('map', {
            zoomControl: false,
            scrollWheelZoom: false // Prevent accidental zooming when scrolling the page
        }).setView([lat, lng], 15);

        // Add zoom control to bottom right so it doesn't overlap text
        L.control.zoom({
            position: 'bottomright'
        }).addTo(map);

        // Use CartoDB Dark Matter tiles for a premium dark look
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);

        // Create custom gold glowing marker
        const goldIcon = L.divIcon({
            className: 'gold-marker',
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });

        // Add marker and popup
        const marker = L.marker([lat, lng], {icon: goldIcon}).addTo(map);

        // Custom popup content with a link to open Google Maps
        const popupContent = `
            <div style="text-align: center;">
                <b style="font-size: 14px; text-transform: uppercase;">REDFIT Parque São Jorge</b><br>
                <span style="font-size: 12px; color: #ccc;">Dentro do Clube Corinthians</span><br>
                <a href="https://www.google.com/maps/search/?api=1&query=${lat},${lng}" target="_blank" style="display: inline-block; margin-top: 8px; padding: 4px 10px; background: #FFD700; color: #000; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 11px; text-transform: uppercase;">Abrir no Google Maps</a>
            </div>
        `;

        marker.bindPopup(popupContent);

        // Optional: Open popup by default when map comes into view
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        marker.openPopup();
                        map.invalidateSize(); // Fix tile loading if container was hidden
                    }, 500);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(mapContainer);
    }
});
