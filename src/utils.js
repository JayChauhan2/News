export function getTimeAgo(dateString) {
    if (!dateString) return "Just Now";

    // Ensure dateString is compatible across browsers (replace space with T for ISO format)
    // Python output: '2026-02-04 17:34:15' -> '2026-02-04T17:34:15'
    const formattedDate = dateString.replace(" ", "T");
    const date = new Date(formattedDate);
    const now = new Date();

    // Check if valid date
    if (isNaN(date.getTime())) return "Just Now";

    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return "Just Now";

    let interval = Math.floor(seconds / 31536000);
    if (interval >= 1) return interval + " year" + (interval === 1 ? "" : "s") + " ago";

    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) return interval + " month" + (interval === 1 ? "" : "s") + " ago";

    interval = Math.floor(seconds / 86400);
    if (interval >= 1) return interval + " day" + (interval === 1 ? "" : "s") + " ago";

    interval = Math.floor(seconds / 3600);
    if (interval >= 1) return interval + " hour" + (interval === 1 ? "" : "s") + " ago";

    interval = Math.floor(seconds / 60);
    if (interval >= 1) return interval + " minute" + (interval === 1 ? "" : "s") + " ago";

    return Math.floor(seconds) + " seconds ago";
}
