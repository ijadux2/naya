// Naya Website JavaScript

// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('naya-theme') || 'dark';
        this.init();
    }

    init() {
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        this.updateThemeToggle();
    }

    toggle() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        localStorage.setItem('naya-theme', this.currentTheme);
        this.updateThemeToggle();
    }

    updateThemeToggle() {
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            const icon = toggle.querySelector('.icon');
            if (this.currentTheme === 'dark') {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m3-20h-6m6 0h-6"></path>';
            } else {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 8.794z"></path>';
            }
        }
    }
}

// Content Loader
class ContentLoader {
    constructor() {
        this.cache = new Map();
        this.currentSection = 'home';
        this.init();
    }

    init() {
        this.loadSection('home');
        this.setupNavigation();
        this.setupHashRouting();
    }

    async loadSection(sectionName) {
        if (this.cache.has(sectionName)) {
            this.renderContent(this.cache.get(sectionName));
            return;
        }

        try {
            const content = await this.fetchContent(sectionName);
            this.cache.set(sectionName, content);
            this.renderContent(content);
        } catch (error) {
            console.error('Failed to load section:', sectionName, error);
            this.renderError(sectionName);
        }
    }

    async fetchContent(sectionName) {
        const response = await fetch(`content/${sectionName}.html`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.text();
    }

    renderContent(content) {
        const container = document.getElementById('content-container');
        if (container) {
            container.innerHTML = content;
            this.highlightCode();
            this.setupInteractions();
        }
    }

    renderError(sectionName) {
        const container = document.getElementById('content-container');
        if (container) {
            container.innerHTML = `
                <div class="container">
                    <div class="alert alert-error">
                        <h3>Content Not Found</h3>
                        <p>The section "${sectionName}" could not be loaded.</p>
                        <p>Please check your internet connection or try again later.</p>
                    </div>
                </div>
            `;
        }
    }

    highlightCode() {
        if (window.hljs) {
            document.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
                block.classList.add('language-naya');
            });
        }
    }

    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.getAttribute('href').substring(1);
                this.loadSection(section);
                this.updateActiveNav(link);
                window.location.hash = section;
            });
        });
    }

    setupHashRouting() {
        window.addEventListener('hashchange', () => {
            const hash = window.location.hash.substring(1);
            if (hash && hash !== this.currentSection) {
                this.loadSection(hash);
                this.updateActiveNavFromHash(hash);
            }
        });

        // Load initial hash
        const initialHash = window.location.hash.substring(1);
        if (initialHash) {
            this.loadSection(initialHash);
            this.updateActiveNavFromHash(initialHash);
        }
    }

    updateActiveNav(activeLink) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        activeLink.classList.add('active');
    }

    updateActiveNavFromHash(hash) {
        const activeLink = document.querySelector(`.nav-link[href="#${hash}"]`);
        if (activeLink) {
            this.updateActiveNav(activeLink);
        }
    }

    setupInteractions() {
        this.setupTabs();
        this.setupCopyButtons();
        this.setupPlayground();
    }

    setupTabs() {
        const tabs = document.querySelectorAll('.tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.getAttribute('data-tab');
                this.switchTab(tabName);
            });
        });
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.querySelector(`[data-content="${tabName}"]`).classList.add('active');
    }

    setupCopyButtons() {
        const copyButtons = document.querySelectorAll('.copy-btn');
        copyButtons.forEach(button => {
            button.addEventListener('click', () => {
                const code = button.getAttribute('data-code');
                this.copyToClipboard(code, button);
            });
        });
    }

    async copyToClipboard(text, button) {
        try {
            await navigator.clipboard.writeText(text);
            this.showCopySuccess(button);
        } catch (err) {
            console.error('Failed to copy text: ', err);
            this.showCopyError(button);
        }
    }

    showCopySuccess(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '✓ Copied!';
        button.classList.add('success');
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('success');
        }, 2000);
    }

    showCopyError(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '✗ Failed';
        button.classList.add('error');
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('error');
        }, 2000);
    }

    setupPlayground() {
        const runButton = document.getElementById('runCode');
        const codeEditor = document.getElementById('codeEditor');
        const outputContainer = document.getElementById('output');

        if (runButton && codeEditor && outputContainer) {
            runButton.addEventListener('click', () => {
                this.runPlaygroundCode(codeEditor.value, outputContainer);
            });
        }
    }

    // Playground specific functions
    loadExample(exampleName) {
        const examples = {
            hello: `func main(): int {
    print("Hello, World!")
    return 0
}`,
            types: `func main(): int {
    // Integer types
    small: int8 = 127
    medium: int32 = 50000
    large: int64 = 1000000
    
    // Unsigned types
    count: uint = 42
    index: uint32 = 100
    
    // Floating point
    pi: float64 = 3.14159
    temperature: float32 = 98.6
    
    // Boolean and string
    is_ready: bool = true
    name: string = "Naya"
    
    // Compile-time constants
    BUFFER_SIZE: comptime int = 1024
    VERSION: comptime string = "1.0.0"
    
    return 0
}`,
            generics: `Vector: type = struct(T: type) {
    data: ptr[T]
    len: uint
    cap: uint
}

func Vector(T: type).new(capacity: uint): Vector(T) {
    data: ptr[T] = alloc(T, capacity)
    return Vector(T){
        data = data,
        len = 0,
        cap = capacity
    }
}

func Vector(T: type).append(self: Vector(T), item: T): void {
    if self.len >= self.cap {
        // Resize logic would go here
        return
    }
    
    self.data[self.len] = item
    self.len = self.len + 1
}

func main(): int {
    // Create vector of integers
    numbers: Vector(int) = Vector(int).new(10)
    
    // Add elements
    numbers.append(10)
    numbers.append(20)
    numbers.append(30)
    
    // Access elements
    for i in 0..numbers.len {
        print("Number {i}: {numbers.get(i)}")
    }
    
    return 0
}`
        };

        if (examples[exampleName]) {
            document.getElementById('codeEditor').value = examples[exampleName];
            this.updateLineNumbers();
        }
    }

    clearEditor() {
        document.getElementById('codeEditor').value = '';
        this.updateLineNumbers();
    }

    updateLineNumbers() {
        const editor = document.getElementById('codeEditor');
        const lineNumbers = document.getElementById('lineNumbers');
        const lines = editor.value.split('\n');
        
        let lineNumbersHTML = '';
        for (let i = 1; i <= lines.length; i++) {
            lineNumbersHTML += i + '\n';
        }
        
        lineNumbers.textContent = lineNumbersHTML;
    }

    syncLineNumbers() {
        const editor = document.getElementById('codeEditor');
        const lineNumbers = document.getElementById('lineNumbers');
        
        // Sync scroll
        lineNumbers.scrollTop = editor.scrollTop;
        
        // Update line numbers
        this.updateLineNumbers();
    }

    async runPlaygroundCode(code, outputContainer) {
        outputContainer.innerHTML = '<div class="spinner"></div>';
        
        try {
            // Simulate compilation delay
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Simulate code execution
            const output = this.simulateCodeExecution(code);
            
            outputContainer.innerHTML = `
                <div class="code-output">
                    <div class="output-header">
                        <span class="output-status success">✓ Compiled Successfully</span>
                        <span class="output-time">${new Date().toLocaleTimeString()}</span>
                    </div>
                    <pre><code class="language-naya">${output}</code></pre>
                </div>
            `;
        } catch (error) {
            outputContainer.innerHTML = `
                <div class="alert alert-error">
                    <strong>Compilation Error:</strong> ${error.message}
                </div>
            `;
        }
    }

    simulateCodeExecution(code) {
        // Simple simulation for demo purposes
        if (code.includes('print')) {
            return 'Hello, Naya!';
        } else if (code.includes('main')) {
            return 'Program executed successfully.';
        } else if (code.includes('Vector')) {
            return 'Vector operations completed successfully.\nNumber 0: 10\nNumber 1: 20\nNumber 2: 30';
        } else if (code.includes('int8') || code.includes('int32') || code.includes('float64')) {
            return 'Type declarations processed successfully.\nAll variables initialized correctly.';
        } else {
            return 'Code compiled and executed successfully.';
        }
    }

    clearOutput() {
        document.getElementById('output').innerHTML = `
            <div class="output-placeholder">
                <svg class="placeholder-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8.5 12.8l5.7 5.7c.8-.8.8-2 0-2.8L8.5 12.8z"/>
                    <path d="M12 2v6m0 4v2m6-10h6m-6 0h-6"/>
                </svg>
                <p>Run your code to see the output here</p>
            </div>
        `;
    }

    downloadCode() {
        const code = document.getElementById('codeEditor').value;
        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'code.naya';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    shareCode() {
        const code = document.getElementById('codeEditor').value;
        
        if (navigator.share) {
            navigator.share({
                title: 'Naya Code',
                text: code
            }).catch(err => {
                console.log('Error sharing:', err);
                this.fallbackShare(code);
            });
        } else {
            this.fallbackShare(code);
        }
    }

    fallbackShare(code) {
        // Copy to clipboard as fallback
        navigator.clipboard.writeText(code).then(() => {
            alert('Code copied to clipboard! You can now share it.');
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    }

    async runPlaygroundCode(code, outputContainer) {
        outputContainer.innerHTML = '<div class="spinner"></div>';
        
        try {
            // Simulate code execution (in real implementation, this would call a backend service)
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            const output = this.simulateCodeExecution(code);
            outputContainer.innerHTML = `
                <div class="code-output">
                    <pre><code>${output}</code></pre>
                </div>
            `;
        } catch (error) {
            outputContainer.innerHTML = `
                <div class="alert alert-error">
                    <strong>Error:</strong> ${error.message}
                </div>
            `;
        }
    }

    simulateCodeExecution(code) {
        // Simple simulation for demo purposes
        if (code.includes('print')) {
            return 'Hello, Naya!';
        } else if (code.includes('main')) {
            return 'Program executed successfully.';
        } else {
            return 'Code compiled and executed.';
        }
    }
}

// Installation Helper
class InstallationHelper {
    constructor() {
        this.detectPlatform();
        this.setupInstallationButtons();
    }

    detectPlatform() {
        const userAgent = navigator.userAgent.toLowerCase();
        const platform = navigator.platform.toLowerCase();

        if (platform.includes('win') || userAgent.includes('win')) {
            this.platform = 'windows';
        } else if (platform.includes('mac') || userAgent.includes('mac')) {
            this.platform = 'macos';
        } else {
            this.platform = 'linux';
        }
    }

    setupInstallationButtons() {
        const buttons = document.querySelectorAll('.install-btn');
        buttons.forEach(button => {
            button.addEventListener('click', () => {
                this.showInstallationInstructions(button.getAttribute('data-platform'));
            });
        });
    }

    showInstallationInstructions(platform) {
        const modal = document.createElement('div');
        modal.className = 'installation-modal';
        modal.innerHTML = this.getInstallationContent(platform);
        
        document.body.appendChild(modal);
        
        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    getInstallationContent(platform) {
        const contents = {
            linux: `
                <div class="modal-content">
                    <h3>Linux Installation</h3>
                    <div class="installation-steps">
                        <div class="step">
                            <div class="step-title">Clone the repository</div>
                            <div class="step-code">git clone https://github.com/username/naya.git</div>
                        </div>
                        <div class="step">
                            <div class="step-title">Run the installer</div>
                            <div class="step-code">./install.sh</div>
                        </div>
                        <div class="step">
                            <div class="step-title">Verify installation</div>
                            <div class="step-code">naya --version</div>
                        </div>
                    </div>
                </div>
            `,
            macos: `
                <div class="modal-content">
                    <h3>macOS Installation</h3>
                    <div class="installation-steps">
                        <div class="step">
                            <div class="step-title">Install dependencies</div>
                            <div class="step-code">brew install python3 gcc make git</div>
                        </div>
                        <div class="step">
                            <div class="step-title">Clone and install</div>
                            <div class="step-code">git clone https://github.com/username/naya.git && cd naya && ./install.sh</div>
                        </div>
                    </div>
                </div>
            `,
            windows: `
                <div class="modal-content">
                    <h3>Windows Installation</h3>
                    <div class="installation-steps">
                        <div class="step">
                            <div class="step-title">PowerShell (Recommended)</div>
                            <div class="step-code">git clone https://github.com/username/naya.git && cd naya && .\\install.ps1</div>
                        </div>
                        <div class="step">
                            <div class="step-title">Command Prompt</div>
                            <div class="step-code">git clone https://github.com/username/naya.git && cd naya && install.bat</div>
                        </div>
                    </div>
                </div>
            `
        };

        return contents[platform] || contents.linux;
    }
}

// Search Functionality
class SearchManager {
    constructor() {
        this.setupSearch();
    }

    setupSearch() {
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');

        if (searchInput && searchResults) {
            searchInput.addEventListener('input', (e) => {
                this.performSearch(e.target.value, searchResults);
            });

            // Close search when clicking outside
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.search-container')) {
                    searchResults.style.display = 'none';
                }
            });
        }
    }

    async performSearch(query, resultsContainer) {
        if (query.length < 2) {
            resultsContainer.style.display = 'none';
            return;
        }

        // Simulate search results (in real implementation, this would call a search API)
        const results = await this.simulateSearch(query);
        this.displaySearchResults(results, resultsContainer);
    }

    async simulateSearch(query) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 200));
        
        const allContent = [
            { title: 'Getting Started', section: 'installation', description: 'Learn how to install Naya' },
            { title: 'Language Specification', section: 'documentation', description: 'Complete language reference' },
            { title: 'Examples', section: 'examples', description: 'Code examples and tutorials' },
            { title: 'Playground', section: 'playground', description: 'Try Naya in your browser' },
            { title: 'Memory Management', section: 'documentation', description: 'Learn about Naya\'s memory safety features' },
            { title: 'Generics', section: 'documentation', description: 'Generic programming in Naya' },
            { title: 'C ABI Compatibility', section: 'documentation', description: 'Using C libraries with Naya' }
        ];

        return allContent.filter(item => 
            item.title.toLowerCase().includes(query.toLowerCase()) ||
            item.description.toLowerCase().includes(query.toLowerCase())
        );
    }

    displaySearchResults(results, container) {
        if (results.length === 0) {
            container.innerHTML = '<div class="search-no-results">No results found</div>';
        } else {
            container.innerHTML = results.map(result => `
                <div class="search-result" onclick="loadSection('${result.section}')">
                    <h4>${result.title}</h4>
                    <p>${result.description}</p>
                    <small>Section: ${result.section}</small>
                </div>
            `).join('');
        }
        
        container.style.display = 'block';
    }
}

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
    const themeManager = new ThemeManager();
    const contentLoader = new ContentLoader();
    const installationHelper = new InstallationHelper();
    const searchManager = new SearchManager();

    // Global functions for onclick handlers
    window.loadSection = (section) => contentLoader.loadSection(section);
    window.toggleTheme = () => themeManager.toggle();

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading states
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
    });

    // Performance monitoring
    if (window.performance) {
        window.addEventListener('load', () => {
            const perfData = window.performance.timing;
            const loadTime = perfData.loadEventEnd - perfData.navigationStart;
            console.log(`Page load time: ${loadTime}ms`);
        });
    }
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Analytics (placeholder)
function trackEvent(eventName, properties = {}) {
    // In real implementation, this would send to analytics service
    console.log('Event:', eventName, properties);
}

function trackPageView(pageName) {
    // In real implementation, this would send to analytics service
    console.log('Page view:', pageName);
}