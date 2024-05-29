// Custom mapping from filter text to tag keys
const filterTagMap = {
    'LLM Classifier': 'LLM',
    'SQL Injection': 'SQL_INJECTION',
    'Cross Site Scripting': 'CROSS_SITE_SCRIPTING',
    // Add more mappings as needed
};

document.addEventListener('DOMContentLoaded', function () {
    const filterList = document.getElementById('filter-list');
    const filterButton = document.querySelector('.status .btn:nth-of-type(2)');
    let selectedFilters = [];

    // Assume all records are rendered on the page, and we can fetch them using data-* attributes
    const records = Array.from(document.querySelectorAll('tbody tr')).map(tr => ({
        element: tr,
        data: JSON.parse(tr.querySelector('td:last-child p').textContent)
    }));

    // Event listener for filter list clicks
    filterList.addEventListener('click', function (event) {
        const target = event.target;
        if (target.tagName === 'A' && target.classList.contains('filter')) {
            event.preventDefault(); // Prevent default behavior
            const li = target.parentElement;
            li.classList.toggle('active');
            const filterText = target.textContent;

            if (li.classList.contains('active')) {
                selectedFilters.push(filterText);
            } else {
                selectedFilters = selectedFilters.filter(filter => filter !== filterText);
            }
            updateFilterButton();
            updateTable();
        }
    });

    // Update the filter button text and bind the close button event
    function updateFilterButton() {
        filterButton.innerHTML = `${selectedFilters.length} filters <span class="close">❎</span>`;
        const closeButton = filterButton.querySelector('.close');
        closeButton.addEventListener('click', function (event) {
            event.stopPropagation();
            selectedFilters = [];
            const activeFilters = filterList.querySelectorAll('li.active');
            activeFilters.forEach(filter => filter.classList.remove('active'));
            updateFilterButton();
            updateTable();
        });
    }

    // Update the table content based on selected filters
    function updateTable() {
        records.forEach(record => {
            const matches = selectedFilters.every(filter => {
                const tagKey = filterTagMap[filter];
                return tagKey && record.data.tag[tagKey];
            });
            record.element.style.display = matches ? '' : 'none';
        });
    }

    // Initial bind
    updateFilterButton();
});