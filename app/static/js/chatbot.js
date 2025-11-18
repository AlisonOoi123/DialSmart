/**
 * DialSmart Chatbot JavaScript
 * Handles chatbot widget interactions and API calls
 */

$(document).ready(function() {
    var sessionId = null;
    var isOpen = false;

    // Toggle chatbot window
    $('#chatbot-toggle').on('click', function() {
        if (isOpen) {
            $('#chatbot-window').fadeOut();
            isOpen = false;
        } else {
            $('#chatbot-window').fadeIn();
            isOpen = true;
            if (!sessionId) {
                sessionId = generateSessionId();
            }
        }
    });

    // Close chatbot window
    $('#chatbot-close').on('click', function() {
        $('#chatbot-window').fadeOut();
        isOpen = false;
    });

    // Send message
    $('#chat-send').on('click', function() {
        sendMessage();
    });

    // Send message on Enter key
    $('#chat-input').on('keypress', function(e) {
        if (e.which === 13) {
            sendMessage();
        }
    });

    // Quick reply buttons
    $('.quick-reply-btn').on('click', function() {
        var message = $(this).text();
        $('#chat-input').val(message);
        sendMessage();
    });

    function sendMessage() {
        var message = $('#chat-input').val().trim();

        if (!message) {
            return;
        }

        // Display user message
        appendMessage(message, 'user');

        // Clear input
        $('#chat-input').val('');

        // Show typing indicator
        showTypingIndicator();

        // Send to API
        $.ajax({
            url: '/api/chat',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                message: message,
                session_id: sessionId
            }),
            success: function(response) {
                hideTypingIndicator();

                if (response.success) {
                    appendMessage(response.response, 'bot');

                    // Handle quick replies
                    if (response.quick_replies && response.quick_replies.length > 0) {
                        appendQuickReplies(response.quick_replies);
                    }

                    // Handle phone recommendations and phone details
                    if ((response.type === 'recommendation' || response.type === 'phone_details') && response.metadata.phones) {
                        appendPhoneCards(response.metadata.phones);
                    }
                } else {
                    appendMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            },
            error: function() {
                hideTypingIndicator();
                appendMessage('Sorry, I could not process your request. Please try again later.', 'bot');
            }
        });
    }

    function appendMessage(message, type) {
        var messageClass = type === 'user' ? 'user-message' : 'bot-message';

        // Convert markdown links to HTML for bot messages
        var processedMessage = message;
        if (type === 'bot') {
            // Convert [text](url) to <a href="url">text</a>
            processedMessage = processedMessage.replace(/\[([^\]]+)\]\(([^)]+)\)/g, function(match, text, url) {
                return `<a href="${escapeHtml(url)}" class="text-primary text-decoration-underline" target="_blank">${escapeHtml(text)}</a>`;
            });
            // Convert **text** to <strong>text</strong>
            processedMessage = processedMessage.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
            // Convert line breaks
            processedMessage = processedMessage.replace(/\n/g, '<br>');
        } else {
            processedMessage = escapeHtml(message);
        }

        var messageHtml = `
            <div class="chat-message ${messageClass}">
                <div class="message-content">${processedMessage}</div>
            </div>
        `;

        $('#chat-messages').append(messageHtml);
        scrollToBottom();
    }

    function appendPhoneCards(phones) {
        var cardsHtml = '<div class="phone-recommendations mt-2">';
        var timestamp = Date.now();
        var cardIds = [];

        phones.forEach(function(phone, index) {
            // Get image URL or use placeholder
            var placeholderUrl = 'https://via.placeholder.com/120x120/e0e0e0/666666?text=No+Image';
            var imageUrl = phone.image || placeholderUrl;
            var brandName = phone.brand || '';
            var displayName = brandName ? `${brandName} ${phone.name}` : phone.name;

            // Generate unique ID for this card
            var cardId = 'phone-card-' + phone.id + '-' + timestamp + '-' + index;
            cardIds.push(cardId);

            cardsHtml += `
                <div class="card mb-2" style="max-width: 100%;">
                    <div class="row g-0">
                        <div class="col-4 position-relative">
                            <div class="phone-img-wrapper" style="position: relative; min-height: 100px; background: #f5f5f5;">
                                <div class="phone-img-loader-${cardId}" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); display: none;">
                                    <div class="spinner-border spinner-border-sm text-primary" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                                <img
                                    id="${cardId}"
                                    data-src="${escapeHtml(imageUrl)}"
                                    src="${escapeHtml(placeholderUrl)}"
                                    class="img-fluid rounded-start phone-card-img"
                                    alt="${escapeHtml(displayName)}"
                                    style="object-fit: cover; height: 100%; width: 100%; min-height: 100px; opacity: 0; transition: opacity 0.3s ease;"
                                    onerror="this.style.opacity='1'; this.src='${placeholderUrl}';">
                            </div>
                        </div>
                        <div class="col-8">
                            <div class="card-body p-2">
                                <h6 class="card-title mb-1">${escapeHtml(displayName)}</h6>
                                <p class="card-text mb-1 small">
                                    <strong class="text-primary">RM ${phone.price.toFixed(2)}</strong>
                                    ${phone.match_score ? `<span class="badge bg-success ms-2">${phone.match_score}% Match</span>` : ''}
                                </p>
                                <a href="/phone/${phone.id}" class="btn btn-sm btn-primary" target="_blank">View Details</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        cardsHtml += '</div>';
        $('#chat-messages').append(cardsHtml);

        // Load images progressively to prevent blinking
        cardIds.forEach(function(cardId) {
            var imgElement = document.getElementById(cardId);
            if (imgElement) {
                var actualImageUrl = imgElement.getAttribute('data-src');
                var loader = document.querySelector('.phone-img-loader-' + cardId);

                // Show loader
                if (loader) loader.style.display = 'block';

                // Create a new image to preload
                var img = new Image();
                img.onload = function() {
                    imgElement.src = actualImageUrl;
                    imgElement.style.opacity = '1';
                    if (loader) loader.style.display = 'none';
                };
                img.onerror = function() {
                    imgElement.style.opacity = '1';
                    if (loader) loader.style.display = 'none';
                };

                // Start loading
                img.src = actualImageUrl;
            }
        });

        scrollToBottom();
    }

    function appendQuickReplies(replies) {
        var repliesHtml = '<div class="quick-replies mt-2 mb-2">';

        replies.forEach(function(reply) {
            repliesHtml += `<button class="btn btn-sm btn-outline-primary me-1 mb-1 dynamic-quick-reply">${escapeHtml(reply)}</button>`;
        });

        repliesHtml += '</div>';
        $('#chat-messages').append(repliesHtml);

        // Bind click event to dynamic quick replies
        $('.dynamic-quick-reply').on('click', function() {
            var message = $(this).text();
            $('#chat-input').val(message);
            sendMessage();
        });

        scrollToBottom();
    }

    function showTypingIndicator() {
        var typingHtml = `
            <div class="chat-message bot-message typing-indicator">
                <div class="message-content">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>
        `;
        $('#chat-messages').append(typingHtml);
        scrollToBottom();
    }

    function hideTypingIndicator() {
        $('.typing-indicator').remove();
    }

    function scrollToBottom() {
        var chatMessages = $('#chat-messages');
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
    }

    function generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    function escapeHtml(text) {
        var map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    // Load chat history on widget open
    function loadChatHistory() {
        $.ajax({
            url: '/api/chat/history',
            data: { session_id: sessionId, limit: 20 },
            success: function(response) {
                if (response.success && response.history.length > 0) {
                    $('#chat-messages').empty();

                    response.history.reverse().forEach(function(chat) {
                        appendMessage(chat.message, 'user');
                        appendMessage(chat.response, 'bot');
                    });
                }
            }
        });
    }

    // Typing animation styles
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            .typing-dot {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background-color: #888;
                margin: 0 2px;
                animation: typing 1.4s infinite;
            }

            .typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }

            .typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }

            @keyframes typing {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.7;
                }
                30% {
                    transform: translateY(-10px);
                    opacity: 1;
                }
            }

            .phone-recommendations .card {
                border: 1px solid #dee2e6;
                transition: all 0.3s ease;
            }

            .phone-recommendations .card:hover {
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                transform: translateY(-2px);
            }

            .phone-img-wrapper {
                overflow: hidden;
            }

            .phone-card-img {
                display: block;
                width: 100%;
            }

            .phone-card-img[src*="placeholder"] {
                background: linear-gradient(45deg, #f5f5f5 25%, #e8e8e8 25%, #e8e8e8 50%, #f5f5f5 50%, #f5f5f5 75%, #e8e8e8 75%, #e8e8e8);
                background-size: 40px 40px;
            }
        `)
        .appendTo('head');
});
