// Expense Tracker Frontend JavaScript

// DOM Elements
const expenseForm = document.getElementById('expenseForm');
const expensesList = document.getElementById('expensesList');
const filterCategory = document.getElementById('filterCategory');
const filterMonth = document.getElementById('filterMonth');
const clearFiltersBtn = document.getElementById('clearFilters');
const refreshBtn = document.getElementById('refreshBtn');
const totalExpenses = document.getElementById('totalExpenses');
const transactionCount = document.getElementById('transactionCount');
const averageExpense = document.getElementById('averageExpense');
const categoryBreakdown = document.getElementById('categoryBreakdown');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadExpenses();
    loadStatistics();
    loadCategories();
    
    // Set today's date as default
    document.getElementById('date').valueAsDate = new Date();
});

// Form submission
expenseForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        description: document.getElementById('description').value.trim(),
        amount: parseFloat(document.getElementById('amount').value),
        category: document.getElementById('category').value.trim(),
        date: document.getElementById('date').value || null
    };
    
    try {
        const response = await fetch('/api/expenses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('Expense added successfully!', 'success');
            expenseForm.reset();
            document.getElementById('date').valueAsDate = new Date();
            loadExpenses();
            loadStatistics();
            loadCategories();
        } else {
            showMessage(data.error || 'Failed to add expense', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
});

// Filter events
filterCategory.addEventListener('change', loadExpenses);
filterMonth.addEventListener('change', loadExpenses);
clearFiltersBtn.addEventListener('click', () => {
    filterCategory.value = '';
    filterMonth.value = '';
    loadExpenses();
});

refreshBtn.addEventListener('click', () => {
    loadExpenses();
    loadStatistics();
    loadCategories();
});

// Load expenses
async function loadExpenses() {
    try {
        const category = filterCategory.value;
        const month = filterMonth.value;
        
        let url = '/api/expenses?';
        if (category) url += `category=${encodeURIComponent(category)}&`;
        if (month) url += `month=${encodeURIComponent(month)}&`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        displayExpenses(data.expenses, data.total);
    } catch (error) {
        showMessage('Error loading expenses: ' + error.message, 'error');
    }
}

// Display expenses
function displayExpenses(expenses, total) {
    if (expenses.length === 0) {
        expensesList.innerHTML = '<div class="empty-state">No expenses found. Add your first expense above!</div>';
        return;
    }
    
    let html = '';
    
    expenses.forEach(expense => {
        const date = new Date(expense.date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        html += `
            <div class="expense-item">
                <div class="expense-date">${date}</div>
                <div class="expense-category">${escapeHtml(expense.category)}</div>
                <div class="expense-description">${escapeHtml(expense.description)}</div>
                <div class="expense-actions">
                    <span class="expense-amount">₹${expense.amount.toFixed(2)}</span>
                    <button class="btn btn-danger" onclick="deleteExpense('${expense.id}')">Delete</button>
                </div>
            </div>
        `;
    });
    
    html += `
        <div class="expense-item" style="background: var(--primary-color); color: white; font-weight: 700; margin-top: 16px;">
            <div></div>
            <div></div>
            <div style="text-align: right;">Total:</div>
            <div style="color: white;">₹${total.toFixed(2)}</div>
        </div>
    `;
    
    expensesList.innerHTML = html;
}

// Delete expense
async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/expenses/${id}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('Expense deleted successfully!', 'success');
            loadExpenses();
            loadStatistics();
            loadCategories();
        } else {
            showMessage(data.error || 'Failed to delete expense', 'error');
        }
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        totalExpenses.textContent = `₹${data.total.toFixed(2)}`;
        transactionCount.textContent = data.count;
        averageExpense.textContent = `₹${data.average.toFixed(2)}`;
        
        // Display category breakdown
        if (Object.keys(data.categories).length === 0) {
            categoryBreakdown.innerHTML = '<p style="color: var(--text-secondary); text-align: center;">No category data available</p>';
            return;
        }
        
        let html = '<h3 style="margin-bottom: 12px; color: var(--text-primary);">By Category:</h3>';
        
        // Sort categories by amount (descending)
        const sortedCategories = Object.entries(data.categories)
            .sort((a, b) => b[1].amount - a[1].amount);
        
        sortedCategories.forEach(([category, info]) => {
            html += `
                <div class="category-item">
                    <div class="category-name">${escapeHtml(category)}</div>
                    <div>
                        <span class="category-amount">₹${info.amount.toFixed(2)}</span>
                        <span class="category-percentage">(${info.percentage}%)</span>
                    </div>
                </div>
            `;
        });
        
        categoryBreakdown.innerHTML = html;
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load categories
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();
        
        // Update category filter dropdown
        filterCategory.innerHTML = '<option value="">All Categories</option>';
        data.categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            filterCategory.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Show message
function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = message;
    
    const firstCard = document.querySelector('.card');
    firstCard.insertBefore(messageDiv, firstCard.firstChild);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

