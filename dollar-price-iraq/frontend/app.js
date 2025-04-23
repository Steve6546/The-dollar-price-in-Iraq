const API_URL = 'http://localhost:8000/api/rates'; // Assuming backend runs on port 8000

function populateTable(data) {
    const tableBody = document.getElementById('rates-table');
    const lastUpdated = document.getElementById('last-updated');
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    // Add new rows
    data.forEach(item => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.city}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.buy}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.sell}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.updated}</td>
        `;
        
        tableBody.appendChild(row);
    });
    
    // Update timestamp
    const now = new Date();
    lastUpdated.textContent = now.toLocaleString('ar-IQ');
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
