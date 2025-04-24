const API_URL = 'http://localhost:8000/api/rates'; // Assuming backend runs on port 8000

function populateTable(data) {
    const tableBody = document.getElementById('rates-table');
    const lastUpdated = document.getElementById('last-updated');
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    // Add new rows
    data.forEach(item => {
        const row = document.createElement('tr');
        
        // Format prices with commas
        const buyPriceFormatted = item.buy_price.toLocaleString('en-US');
        const sellPriceFormatted = item.sell_price.toLocaleString('en-US');
        // Format timestamp
        const updatedTime = new Date(item.last_updated).toLocaleTimeString('ar-IQ', { hour: '2-digit', minute: '2-digit', hour12: true });
        const updatedDate = new Date(item.last_updated).toLocaleDateString('ar-IQ', { year: 'numeric', month: '2-digit', day: '2-digit' });

        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.city}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${buyPriceFormatted}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${sellPriceFormatted}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${updatedDate} ${updatedTime}</td>
        `;

        const sourceRow = document.createElement('tr');
        sourceRow.innerHTML = `
            <td colspan="4" class="px-6 py-2 whitespace-nowrap text-sm text-gray-500 text-center">
                المصدر: ${item.source}
            </td>
        `;

        tableBody.appendChild(row);
        tableBody.appendChild(sourceRow);
    });

    // Find the most recent update time from the data
    let mostRecentUpdate = null;
    if (data.length > 0) {
        // Filter out any invalid dates before finding the max
        const validDates = data
            .map(item => new Date(item.last_updated))
            .filter(date => !isNaN(date.getTime()));

        if (validDates.length > 0) {
            mostRecentUpdate = new Date(Math.max.apply(null, validDates));
        }
    }

    // Update the overall timestamp display
    if (mostRecentUpdate) {
        lastUpdated.textContent = mostRecentUpdate.toLocaleString('ar-IQ', { dateStyle: 'medium', timeStyle: 'short' });
    } else {
        lastUpdated.textContent = 'غير متوفر'; // Or keep 'جار التحميل...' if preferred
    }
}

async function fetchRates() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching rates:", error);
        // Return empty array or handle error appropriately
        return []; 
    }
}

async function updateRates() {
    const ratesData = await fetchRates();
    if (ratesData && ratesData.length > 0) {
        populateTable(ratesData);
    } else {
        // Handle case where data fetch failed or returned empty
        const tableBody = document.getElementById('rates-table');
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-red-500">فشل تحميل البيانات. حاول مرة أخرى لاحقًا.</td></tr>';
        document.getElementById('last-updated').textContent = 'خطأ';
    }
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    updateRates(); // Fetch and display rates on load
    
    // Set up auto-refresh (every 10 minutes)
    setInterval(updateRates, 10 * 60 * 1000); 
});
