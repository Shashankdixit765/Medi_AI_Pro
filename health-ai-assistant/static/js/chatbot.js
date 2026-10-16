/**
 * MediAI Pro — Conversational Medical Chatbot (MediBot AI)
 * Architected by Shashank Dixit
 */

const Chatbot = {
    history: [],

    init() {
        this.setupChatForm();
        this.setupPromptChips();
        this.setupClearChat();
    },

    setupChatForm() {
        const form = document.getElementById('chat-form');
        const input = document.getElementById('chat-input');

        if (form && input) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const msg = input.value.trim();
                if (!msg) return;

                input.value = '';
                await this.sendMessage(msg);
            });
        }
    },

    setupPromptChips() {
        const chips = document.querySelectorAll('.chat-prompt-pill');
        chips.forEach(chip => {
            chip.addEventListener('click', async () => {
                const promptText = chip.getAttribute('data-prompt');
                if (promptText) {
                    await this.sendMessage(promptText);
                }
            });
        });
    },

    setupClearChat() {
        const clearBtn = document.getElementById('clear-chat-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.history = [];
                const messagesContainer = document.getElementById('chat-messages-container');
                if (messagesContainer) {
                    messagesContainer.innerHTML = `
                        <div class="flex items-start gap-3">
                            <div class="w-8 h-8 rounded-full bg-sky-600 text-white flex items-center justify-center text-sm shadow-sm flex-shrink-0">
                                <i class="fa-solid fa-robot"></i>
                            </div>
                            <div class="chat-bubble-bot p-4 shadow-sm max-w-[85%] text-sm leading-relaxed">
                                <p class="font-bold text-sky-600 dark:text-sky-400 mb-1">MediBot AI Assistant</p>
                                <p>Chat cleared! How can I assist you with your health, medications, symptoms, or lab reports today?</p>
                            </div>
                        </div>
                    `;
                }
                App.showToast('Conversation reset', 'info');
            });
        }
    },

    async sendMessage(messageText) {
        const messagesContainer = document.getElementById('chat-messages-container');
        if (!messagesContainer) return;

        // Append User Message
        const now = new Date();
        const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        const userMsgDiv = document.createElement('div');
        userMsgDiv.className = 'flex items-start justify-end gap-3';
        userMsgDiv.innerHTML = `
            <div class="chat-bubble-user p-4 shadow-sm max-w-[85%] text-sm leading-relaxed">
                <p class="font-bold text-white/90 text-xs mb-1 text-right">You (${timeStr})</p>
                <p class="whitespace-pre-wrap">${this.escapeHtml(messageText)}</p>
            </div>
            <div class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 flex items-center justify-center text-sm shadow-sm flex-shrink-0">
                <i class="fa-solid fa-user"></i>
            </div>
        `;
        messagesContainer.appendChild(userMsgDiv);
        this.scrollToBottom();

        // Push to history
        this.history.push({ sender: 'user', text: messageText });

        // Show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.id = 'bot-typing-indicator';
        typingDiv.className = 'flex items-start gap-3';
        typingDiv.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-sky-600 text-white flex items-center justify-center text-sm shadow-sm flex-shrink-0">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="chat-bubble-bot p-3 shadow-sm max-w-[85%] text-sm flex items-center gap-2 text-slate-400">
                <span class="inline-block w-2 h-2 rounded-full bg-sky-500 animate-ping"></span>
                <span class="text-xs">MediBot is analyzing medical context...</span>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: messageText,
                    history: this.history,
                    api_key: App.apiKey || null
                })
            });

            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const json = await res.json();
            const botReply = json.reply || "I apologize, but I could not formulate a response. Please try asking again.";

            // Remove typing indicator
            document.getElementById('bot-typing-indicator')?.remove();

            // Append Bot Message
            const botMsgDiv = document.createElement('div');
            botMsgDiv.className = 'flex items-start gap-3';
            botMsgDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-sky-600 text-white flex items-center justify-center text-sm shadow-sm flex-shrink-0">
                    <i class="fa-solid fa-robot"></i>
                </div>
                <div class="chat-bubble-bot p-4 shadow-sm max-w-[85%] text-sm leading-relaxed">
                    <div class="flex items-center justify-between mb-1">
                        <span class="font-bold text-sky-600 dark:text-sky-400 text-xs">MediBot AI (${timeStr})</span>
                        <span class="text-[10px] text-slate-400">Clinical Support</span>
                    </div>
                    <div class="bot-markdown-content text-slate-800 dark:text-slate-200">
                        ${this.formatMarkdown(botReply)}
                    </div>
                </div>
            `;
            messagesContainer.appendChild(botMsgDiv);
            this.history.push({ sender: 'bot', text: botReply });
            this.scrollToBottom();

        } catch (err) {
            document.getElementById('bot-typing-indicator')?.remove();
            const errDiv = document.createElement('div');
            errDiv.className = 'flex items-start gap-3';
            errDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-rose-600 text-white flex items-center justify-center text-sm shadow-sm flex-shrink-0">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                </div>
                <div class="chat-bubble-bot p-3 border-rose-200 text-rose-600 text-xs shadow-sm max-w-[85%]">
                    Communication error with AI service: ${err.message}. Please check connection or API key.
                </div>
            `;
            messagesContainer.appendChild(errDiv);
            this.scrollToBottom();
        }
    },

    scrollToBottom() {
        const container = document.getElementById('chat-messages-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    formatMarkdown(text) {
        // Convert basic markdown: bold **text**, bullets, newlines
        let formatted = this.escapeHtml(text);
        
        // Bold
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong class="text-slate-900 dark:text-white font-bold">$1</strong>');
        
        // Bullet points starting with • or * or -
        formatted = formatted.replace(/^[•\*\-]\s+(.*)$/gm, '<li class="ml-4 list-disc my-0.5">$1</li>');
        
        // Numbered lists
        formatted = formatted.replace(/^\d+\.\s+(.*)$/gm, '<li class="ml-4 list-decimal my-0.5">$1</li>');

        // Line breaks
        formatted = formatted.replace(/\n\n/g, '<div class="my-2"></div>');
        formatted = formatted.replace(/\n/g, '<br>');

        return formatted;
    }
};

window.addEventListener('DOMContentLoaded', () => {
    Chatbot.init();
});
