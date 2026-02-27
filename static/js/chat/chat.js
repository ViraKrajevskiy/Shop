/* Scroll chat to bottom on load */
document.addEventListener('DOMContentLoaded', function() {
    const el = document.getElementById('chatMessages');
    if (el) el.scrollTo(0, 99999);
});
