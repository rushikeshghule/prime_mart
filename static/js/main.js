// Main JavaScript for Prime Mart

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add hover effect for product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.querySelector('.card-img-top')?.classList.add('hovered');
        });
        card.addEventListener('mouseleave', function() {
            this.querySelector('.card-img-top')?.classList.remove('hovered');
        });
    });

    // Countdown timer for deal of the day (if present)
    const countdownContainer = document.querySelector('.countdown');
    if (countdownContainer) {
        // Set the countdown date to 24 hours from now
        const countDownDate = new Date();
        countDownDate.setHours(countDownDate.getHours() + 23);
        countDownDate.setMinutes(countDownDate.getMinutes() + 45);
        countDownDate.setSeconds(countDownDate.getSeconds() + 19);

        // Update the countdown every 1 second
        const countdownTimer = setInterval(function() {
            // Get current date and time
            const now = new Date().getTime();
            
            // Find the distance between now and the countdown date
            const distance = countDownDate - now;
            
            // Time calculations for hours, minutes and seconds
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            // Display the result
            const hoursElem = document.querySelector('.countdown-item:nth-child(1) .countdown-number');
            const minutesElem = document.querySelector('.countdown-item:nth-child(2) .countdown-number');
            const secondsElem = document.querySelector('.countdown-item:nth-child(3) .countdown-number');
            
            if (hoursElem) hoursElem.textContent = hours.toString().padStart(2, '0');
            if (minutesElem) minutesElem.textContent = minutes.toString().padStart(2, '0');
            if (secondsElem) secondsElem.textContent = seconds.toString().padStart(2, '0');
            
            // If the countdown is finished, clear the interval
            if (distance < 0) {
                clearInterval(countdownTimer);
                if (countdownContainer) {
                    countdownContainer.innerHTML = "EXPIRED";
                }
            }
        }, 1000);
    }

    // Shopping cart quantity handling
    const quantityBtns = document.querySelectorAll('.quantity-btn');
    quantityBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const currentValue = parseInt(input.value);
            
            if (this.classList.contains('decrement') && currentValue > 1) {
                input.value = currentValue - 1;
            } else if (this.classList.contains('increment')) {
                input.value = currentValue + 1;
            }
        });
    });

    // Newsletter subscription form
    const newsletterForm = document.querySelector('.newsletter-section form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            
            if (emailInput && emailInput.value) {
                // Simulate submission
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Subscribing...';
                    submitBtn.disabled = true;
                }
                
                // Simulate success after 1 second
                setTimeout(() => {
                    emailInput.value = '';
                    if (submitBtn) {
                        submitBtn.innerHTML = 'Subscribe';
                        submitBtn.disabled = false;
                    }
                    
                    // Create success alert
                    const alertDiv = document.createElement('div');
                    alertDiv.className = 'alert alert-success mt-3';
                    alertDiv.textContent = 'Thank you for subscribing to our newsletter!';
                    newsletterForm.parentElement.appendChild(alertDiv);
                    
                    // Remove alert after 3 seconds
                    setTimeout(() => {
                        alertDiv.remove();
                    }, 3000);
                }, 1000);
            }
        });
    }

    // Product filters 
    initializeFilters();
    
    // Initialize product image hover effect
    initializeProductHover();
    
    // Initialize countdown timer if exists
    initializeCountdown();

    // Find all wishlist buttons
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    
    wishlistButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Check if user is logged in by checking if there's a URL in the href
            const url = this.getAttribute('href');
            if (!url || url === '#') {
                // User not logged in or button not properly set up
                return; // Let default behavior happen (redirect to login)
            }
            
            // If we got here, we can handle the AJAX request
            e.preventDefault();
            
            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'added') {
                    this.classList.add('active');
                    this.querySelector('i').classList.remove('far');
                    this.querySelector('i').classList.add('fas');
                    
                    // Update wishlist count in navbar
                    updateWishlistCount(1);
                } else if (data.status === 'removed') {
                    this.classList.remove('active');
                    this.querySelector('i').classList.remove('fas');
                    this.querySelector('i').classList.add('far');
                    
                    // Update wishlist count in navbar
                    updateWishlistCount(-1);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    
    // Function to update wishlist count in navbar
    function updateWishlistCount(change) {
        const wishlistCountBadge = document.querySelector('.fa-heart + .badge');
        if (wishlistCountBadge) {
            let currentCount = parseInt(wishlistCountBadge.textContent) || 0;
            if (!isNaN(currentCount)) {
                currentCount += change;
                if (currentCount > 0) {
                    wishlistCountBadge.textContent = currentCount;
                    wishlistCountBadge.classList.remove('d-none');
                } else {
                    wishlistCountBadge.textContent = '';
                    wishlistCountBadge.classList.add('d-none');
                }
            }
        }
    }
});

// Filter functionality
function initializeFilters() {
    const filterForm = document.getElementById('filter-form');
    if (!filterForm) return;
    
    // Price range slider
    const priceRange = document.getElementById('price-range');
    const priceOutput = document.getElementById('price-value');
    
    if (priceRange && priceOutput) {
        priceOutput.textContent = '₹' + priceRange.value;
        
        priceRange.addEventListener('input', function() {
            priceOutput.textContent = '₹' + this.value;
        });
    }
    
    // Size filters
    const sizeCheckboxes = document.querySelectorAll('.size-filter');
    sizeCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', applyFilters);
    });
    
    // Color filters
    const colorCheckboxes = document.querySelectorAll('.color-filter');
    colorCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', applyFilters);
    });
    
    // Brand filters
    const brandCheckboxes = document.querySelectorAll('.brand-filter');
    brandCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', applyFilters);
    });
    
    // Discount filters
    const discountCheckboxes = document.querySelectorAll('.discount-filter');
    discountCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', applyFilters);
    });
    
    // Sort selector
    const sortSelector = document.getElementById('sort-selector');
    if (sortSelector) {
        sortSelector.addEventListener('change', applyFilters);
    }
    
    // Reset filters
    const resetBtn = document.getElementById('reset-filters');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetFilters);
    }
    
    // Apply filters button
    const applyBtn = document.getElementById('apply-filters');
    if (applyBtn) {
        applyBtn.addEventListener('click', function(e) {
            e.preventDefault();
            applyFilters();
        });
    }
}

function applyFilters() {
    const products = document.querySelectorAll('.product-card');
    if (!products.length) return;
    
    // Get selected sizes
    const selectedSizes = Array.from(document.querySelectorAll('.size-filter:checked')).map(cb => cb.value);
    
    // Get selected colors
    const selectedColors = Array.from(document.querySelectorAll('.color-filter:checked')).map(cb => cb.value);
    
    // Get selected brands
    const selectedBrands = Array.from(document.querySelectorAll('.brand-filter:checked')).map(cb => cb.value);
    
    // Get selected discount percentages (for sale page)
    const selectedDiscounts = Array.from(document.querySelectorAll('.discount-filter:checked')).map(cb => parseInt(cb.value));
    
    // Get price range
    const priceRange = document.getElementById('price-range');
    const maxPrice = priceRange ? parseInt(priceRange.value) : 10000;
    
    // Filter products
    let visibleCount = 0;
    
    products.forEach(product => {
        const productSize = product.dataset.size;
        const productColor = product.dataset.color;
        const productBrand = product.dataset.brand;
        const productPrice = parseInt(product.dataset.price);
        const productDiscount = product.dataset.discount ? parseInt(product.dataset.discount) : 0;
        
        let isVisible = true;
        
        // Check size filter
        if (selectedSizes.length > 0 && !selectedSizes.includes(productSize)) {
            isVisible = false;
        }
        
        // Check color filter
        if (isVisible && selectedColors.length > 0 && !selectedColors.includes(productColor)) {
            isVisible = false;
        }
        
        // Check brand filter
        if (isVisible && selectedBrands.length > 0 && !selectedBrands.includes(productBrand)) {
            isVisible = false;
        }
        
        // Check discount filter (for sale page)
        if (isVisible && selectedDiscounts.length > 0) {
            let discountMatch = false;
            for (const minDiscount of selectedDiscounts) {
                if (productDiscount >= minDiscount) {
                    discountMatch = true;
                    break;
                }
            }
            if (!discountMatch) {
                isVisible = false;
            }
        }
        
        // Check price filter
        if (isVisible && productPrice > maxPrice) {
            isVisible = false;
        }
        
        // Apply visibility
        if (isVisible) {
            product.classList.remove('d-none');
            visibleCount++;
        } else {
            product.classList.add('d-none');
        }
    });
    
    // Update product count
    updateProductCount(visibleCount);
    
    // Apply sorting if needed
    applySorting();
}

function applySorting() {
    const sortSelector = document.getElementById('sort-selector');
    if (!sortSelector) return;
    
    const sortValue = sortSelector.value;
    const productsContainer = document.querySelector('.products-container');
    const products = Array.from(document.querySelectorAll('.product-card:not(.d-none)'));
    
    if (products.length === 0 || !productsContainer) return;
    
    // Sort products based on selection
    products.sort((a, b) => {
        const aPrice = parseInt(a.dataset.price);
        const bPrice = parseInt(b.dataset.price);
        const aDiscount = parseInt(a.dataset.discount || 0);
        const bDiscount = parseInt(b.dataset.discount || 0);
        
        if (sortValue === 'price-low-high') {
            return aPrice - bPrice;
        } else if (sortValue === 'price-high-low') {
            return bPrice - aPrice;
        } else if (sortValue === 'newest') {
            const aDate = new Date(a.dataset.created);
            const bDate = new Date(b.dataset.created);
            return bDate - aDate;
        } else if (sortValue === 'discount-high-low') {
            return bDiscount - aDiscount;
        }
        
        return 0;
    });
    
    // Re-append products in sorted order
    products.forEach(product => {
        productsContainer.appendChild(product);
    });
}

function resetFilters() {
    // Reset checkboxes
    document.querySelectorAll('.size-filter, .color-filter, .brand-filter, .discount-filter').forEach(cb => {
        cb.checked = false;
    });
    
    // Reset price range
    const priceRange = document.getElementById('price-range');
    if (priceRange) {
        priceRange.value = priceRange.max;
        const priceOutput = document.getElementById('price-value');
        if (priceOutput) {
            priceOutput.textContent = '₹' + priceRange.value;
        }
    }
    
    // Reset sort
    const sortSelector = document.getElementById('sort-selector');
    if (sortSelector) {
        sortSelector.value = 'featured';
    }
    
    // Show all products
    document.querySelectorAll('.product-card').forEach(product => {
        product.classList.remove('d-none');
    });
    
    // Update product count
    const allProducts = document.querySelectorAll('.product-card').length;
    updateProductCount(allProducts);
}

function updateProductCount(count) {
    const countElement = document.getElementById('product-count');
    if (countElement) {
        countElement.textContent = count;
    }
}

// Product image hover effect
function initializeProductHover() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        const img = card.querySelector('.card-img-top');
        if (!img) return;
        
        const originalSrc = img.src;
        const hoverSrc = img.dataset.hover;
        
        if (hoverSrc) {
            card.addEventListener('mouseenter', () => {
                img.src = hoverSrc;
                img.classList.add('hovered');
            });
            
            card.addEventListener('mouseleave', () => {
                img.src = originalSrc;
                img.classList.remove('hovered');
            });
        }
    });
}

// Countdown timer
function initializeCountdown() {
    const countdownElement = document.querySelector('.countdown');
    if (!countdownElement) return;
    
    // Set the target date (24 hours from now)
    const targetDate = new Date();
    targetDate.setHours(targetDate.getHours() + 23);
    targetDate.setMinutes(targetDate.getMinutes() + 59);
    targetDate.setSeconds(targetDate.getSeconds() + 59);
    
    function updateCountdown() {
        const currentDate = new Date();
        const difference = targetDate - currentDate;
        
        if (difference <= 0) {
            // Reset countdown when it reaches 0
            targetDate.setHours(targetDate.getHours() + 24);
            return;
        }
        
        const hours = Math.floor(difference / (1000 * 60 * 60));
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);
        
        document.querySelector('.countdown-item:nth-child(1) .countdown-number').textContent = hours.toString().padStart(2, '0');
        document.querySelector('.countdown-item:nth-child(2) .countdown-number').textContent = minutes.toString().padStart(2, '0');
        document.querySelector('.countdown-item:nth-child(3) .countdown-number').textContent = seconds.toString().padStart(2, '0');
    }
    
    // Update the countdown every second
    updateCountdown();
    setInterval(updateCountdown, 1000);
} 