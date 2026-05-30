/**
 * TravelEase - Main JavaScript
 * Premium Travel Platform Interactions
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavigation();
    initScrollEffects();
    initMobileMenu();
    initSmoothScroll();
    initCounterAnimation();
    initReviewTabs();
    initImageGallery();
    initScrollReveal();

    // Ensure navbar container is visible (prevents #main staying hidden)
    const main = document.getElementById('main');
    if (main) {
        // Navbar visibility regression guard:
        // Some CSS/animations may hide/shift #main (wrapper around the fixed header)
        // — restore safe defaults.
        main.classList.add('revealed');
        main.style.opacity = '1';
        main.style.visibility = 'visible';
        main.style.transform = 'none';
        // Ensure the header layer isn't covered by content
        main.style.position = 'relative';
    }

});

/**
 * Navigation - Header scroll behavior
 */
function initNavigation() {
    const header = document.getElementById('main-header');
    if (!header) return;

    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        // Add/remove scrolled class
        if (currentScroll > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });
}

/**
 * Mobile Menu Toggle
 */
function toggleMenu() {
    const middle = document.getElementById('nav-middle');
    const toggle = document.querySelector('.menu-toggle');
    
    if (!middle || !toggle) return;

    middle.classList.toggle('active');
    
    // Toggle icon between bars and times (X)
    const icon = toggle.querySelector('i');
    if (middle.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
        document.body.style.overflow = 'hidden'; // Prevent scrolling when menu is open
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
        document.body.style.overflow = '';
    }
}

function initMobileMenu() {
    // Close menu when clicking on a link
    const navLinks = document.querySelectorAll('#nav-menu li a');
    const middle = document.getElementById('nav-middle');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (middle && middle.classList.contains('active')) {
                toggleMenu();
            }
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (middle && middle.classList.contains('active')) {
            if (!middle.contains(e.target) && !e.target.closest('.menu-toggle')) {
                toggleMenu();
            }
        }
    });
}

/**
 * Scroll Effects
 */
function initScrollEffects() {
    // Add reveal animation to sections as they come into view
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                
                // Add staggered animation to children if they exist
                const children = entry.target.querySelectorAll('.scroll-reveal');
                children.forEach((child, index) => {
                    setTimeout(() => {
                        child.classList.add('revealed');
                    }, index * 100);
                });
            }
        });
    }, observerOptions);

    // Observe sections
    document.querySelectorAll('section').forEach(section => {
        section.classList.add('scroll-reveal');
        observer.observe(section);
    });
}

/**
 * Scroll Reveal Animation
 */
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.scroll-reveal');
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));
}

/**
 * Smooth Scroll for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                const headerHeight = document.querySelector('header')?.offsetHeight || 80;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Counter Animation for Stats Section
 */
function initCounterAnimation() {
    const counters = document.querySelectorAll('count[data-target]');
    
    if (counters.length === 0) return;

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => counterObserver.observe(counter));
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target'));
    const duration = 2000; // 2 seconds
    const step = target / (duration / 16); // 60fps
    let current = 0;

    const updateCounter = () => {
        current += step;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };

    updateCounter();
}

/**
 * Review Tabs - Switch between reviews
 */
function initReviewTabs() {
    const userBoxes = document.querySelectorAll('.user-box');
    const reviewContents = document.querySelectorAll('.review-content');
    
    if (userBoxes.length === 0) return;

    userBoxes.forEach((box, index) => {
        box.addEventListener('click', function() {
            // Remove active class from all
            userBoxes.forEach(b => b.classList.remove('active'));
            reviewContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked
            this.classList.add('active');
            
            // Show corresponding review
            const userId = this.getAttribute('data-user-id');
            const targetReview = document.getElementById(userId);
            if (targetReview) {
                targetReview.classList.add('active');
            }
        });
    });
}

/**
 * Image Gallery - Swap main image with thumbnail
 */
function initImageGallery() {
    // This function is called by onclick in HTML, but we also initialize
    // any gallery functionality here if needed
}

function swapImage(thumbnail) {
    const mainImage = document.getElementById('mainImage');
    if (!mainImage) return;
    
    const thumbnailImg = thumbnail.querySelector('img');
    if (!thumbnailImg) return;
    
    // Fade out
    mainImage.style.opacity = '0';
    
    setTimeout(() => {
        // Change source
        mainImage.src = thumbnailImg.src;
        mainImage.alt = thumbnailImg.alt;
        
        // Fade in
        mainImage.style.opacity = '1';
        
        // Update active state
        document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
        thumbnail.classList.add('active');
    }, 200);
}

/**
 * Form Validation Enhancement
 */
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    
    inputs.forEach(input => {
        // Remove existing error states
        input.classList.remove('error');
        const errorMsg = input.parentElement.querySelector('.error-message');
        if (errorMsg) errorMsg.remove();
        
        // Check validity
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
            
            // Add error message
            const error = document.createElement('span');
            error.className = 'error-message';
            error.textContent = 'This field is required';
            input.parentElement.appendChild(error);
        }
        
        // Email validation
        if (input.type === 'email' && input.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                isValid = false;
                input.classList.add('error');
                
                const error = document.createElement('span');
                error.className = 'error-message';
                error.textContent = 'Please enter a valid email address';
                input.parentElement.appendChild(error);
            }
        }
    });
    
    return isValid;
}

/**
 * Toast Notifications
 */
function showToast(message, type = 'info', duration = 3000) {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => toast.remove());
    
    // Create toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${getToastIcon(type)}</span>
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    // Add styles
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function getToastIcon(type) {
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    return icons[type] || icons.info;
}

/**
 * Lazy Loading for Images
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

/**
 * Parallax Effect
 */
function initParallax() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    if (parallaxElements.length === 0) return;

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.parallax || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

/**
 * Accordion / Toggle functionality
 */
function initAccordion() {
    const accordionTriggers = document.querySelectorAll('.accordion-trigger');
    
    accordionTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const isOpen = content.style.maxHeight;
            
            // Close all other accordions
            document.querySelectorAll('.accordion-content').forEach(el => {
                el.style.maxHeight = null;
            });
            
            // Toggle current
            if (!isOpen) {
                content.style.maxHeight = content.scrollHeight + 'px';
            }
        });
    });
}

/**
 * Slider / Carousel functionality
 */
let currentSlide = 0;

function moveSlide(direction) {
    const slider = document.querySelector('.slider');
    if (!slider) return;
    
    const slides = slider.querySelectorAll('.slide');
    const totalSlides = slides.length;
    
    if (totalSlides === 0) return;
    
    currentSlide += direction;
    
    if (currentSlide >= totalSlides) {
        currentSlide = 0;
    } else if (currentSlide < 0) {
        currentSlide = totalSlides - 1;
    }
    
    slider.style.transform = `translateX(-${currentSlide * 100}%)`;
}

// Auto-advance slider if exists
function initSlider() {
    const slider = document.querySelector('.slider');
    if (!slider) return;
    
    const slides = slider.querySelectorAll('.slide');
    if (slides.length <= 1) return;
    
    // Auto advance every 5 seconds
    setInterval(() => {
        moveSlide(1);
    }, 5000);
}

/**
 * Search functionality enhancement
 */
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    
    if (!searchInput || !searchButton) return;
    
    // Search on button click
    searchButton.addEventListener('click', performSearch);
    
    // Search on Enter key
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // Live search (optional - debounce for performance)
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            if (this.value.length >= 3) {
                performLiveSearch(this.value);
            }
        }, 300);
    });
}

function performSearch() {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) return;

    const searchTerm = searchInput.value.toLowerCase().trim();

    // If query is empty, restore all cards (home/all-packages must still show)
    const packageCards = document.querySelectorAll('.package-card');
    if (!searchTerm) {
        packageCards.forEach(card => {
            card.style.display = '';
            card.style.animation = '';
        });
        return;
    }

    packageCards.forEach(card => {
        const nameEl = card.querySelector('h3');
        const name = (nameEl?.textContent || '').toLowerCase();

        // All redesigned package cards keep description inside card-front paragraph
        const descEl = card.querySelector('.card-front p') || card.querySelector('p');
        const description = (descEl?.textContent || '').toLowerCase();

        if (name.includes(searchTerm) || description.includes(searchTerm)) {
            card.style.display = '';
            card.style.animation = 'fadeIn 0.3s ease';
        } else {
            card.style.display = 'none';
        }
    });
}


function performLiveSearch(term) {
    // Implement live search with AJAX if needed
    console.log('Live search:', term);
}

/**
 * Initialize all components on page load
 */
window.addEventListener('load', function() {
    // Remove loading state
    document.body.classList.remove('loading');
    
    // Initialize remaining components
    initSlider();
    initSearch();
    initLazyLoading();
    initParallax();
    initAccordion();
});

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Utility: Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for global access (if needed)
window.toggleMenu = toggleMenu;
window.swapImage = swapImage;
window.moveSlide = moveSlide;
window.showToast = showToast;
window.validateForm = validateForm;