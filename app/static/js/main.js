/**
 * DialSmart Main JavaScript
 * Handles general UI interactions and utilities
 */

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Form validation
    (function () {
        'use strict';
        var forms = document.querySelectorAll('.needs-validation');
        Array.prototype.slice.call(forms).forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    })();

    // Search autocomplete
    $('#navbar-search').on('input', function() {
        var query = $(this).val();
        if (query.length >= 2) {
            $.ajax({
                url: '/api/phones/search',
                data: { q: query, limit: 5 },
                success: function(data) {
                    // Handle autocomplete results
                    // Implementation depends on UI library
                }
            });
        }
    });

    // Phone comparison checkbox handling
    var compareList = [];

    $('.compare-checkbox').on('change', function() {
        var phoneId = $(this).data('phone-id');

        if ($(this).is(':checked')) {
            if (compareList.length < 2) {
                compareList.push(phoneId);
            } else {
                $(this).prop('checked', false);
                alert('You can only compare 2 phones at a time.');
            }
        } else {
            compareList = compareList.filter(id => id !== phoneId);
        }

        updateCompareButton();
    });

    function updateCompareButton() {
        if (compareList.length === 2) {
            $('#compare-btn').prop('disabled', false);
            $('#compare-btn').removeClass('btn-secondary').addClass('btn-primary');
        } else {
            $('#compare-btn').prop('disabled', true);
            $('#compare-btn').removeClass('btn-primary').addClass('btn-secondary');
        }
    }

    $('#compare-btn').on('click', function() {
        if (compareList.length === 2) {
            window.location.href = `/phone/compare?phone1=${compareList[0]}&phone2=${compareList[1]}`;
        }
    });

    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Price range slider
    $('#price-range').on('input', function() {
        var value = $(this).val();
        $('#price-value').text('RM ' + value);
    });

    // Filter accordion
    $('.filter-toggle').on('click', function() {
        $(this).find('.bi').toggleClass('bi-chevron-down bi-chevron-up');
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if( target.length ) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });

    // Phone details image gallery
    $('.gallery-thumbnail').on('click', function() {
        var newSrc = $(this).attr('src');
        $('#main-image').attr('src', newSrc);
        $('.gallery-thumbnail').removeClass('active');
        $(this).addClass('active');
    });

    // Loading overlay
    function showLoading() {
        $('body').append('<div id="loading-overlay" class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" style="background: rgba(0,0,0,0.5); z-index: 9999;"><div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div></div>');
    }

    function hideLoading() {
        $('#loading-overlay').remove();
    }

    // AJAX form submissions
    $('.ajax-form').on('submit', function(e) {
        e.preventDefault();
        showLoading();

        var formData = $(this).serialize();
        var url = $(this).attr('action');

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            success: function(response) {
                hideLoading();
                if (response.success) {
                    // Handle success
                    if (response.redirect) {
                        window.location.href = response.redirect;
                    }
                } else {
                    alert(response.message || 'An error occurred');
                }
            },
            error: function() {
                hideLoading();
                alert('An error occurred. Please try again.');
            }
        });
    });

    // Rating stars
    $('.rating-star').on('click', function() {
        var rating = $(this).data('rating');
        $(this).prevAll('.rating-star').addBack().addClass('text-warning');
        $(this).nextAll('.rating-star').removeClass('text-warning');
        $('input[name="rating"]').val(rating);
    });

    // Copy to clipboard
    $('.copy-btn').on('click', function() {
        var text = $(this).data('copy');
        navigator.clipboard.writeText(text).then(function() {
            alert('Copied to clipboard!');
        });
    });

    // Back to top button
    var backToTop = $('<button id="back-to-top" class="btn btn-primary position-fixed bottom-0 end-0 m-4" style="display: none; z-index: 999;"><i class="bi bi-arrow-up"></i></button>');
    $('body').append(backToTop);

    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 300) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }
    });

    $('#back-to-top').on('click', function() {
        $('html, body').animate({ scrollTop: 0 }, 800);
    });

    // Print functionality
    $('.print-btn').on('click', function() {
        window.print();
    });

    // Share functionality
    $('.share-btn').on('click', function() {
        if (navigator.share) {
            navigator.share({
                title: document.title,
                url: window.location.href
            });
        } else {
            alert('Sharing is not supported on this browser.');
        }
    });
});

// Utility functions
function formatPrice(price) {
    return 'RM ' + price.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-MY', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}
