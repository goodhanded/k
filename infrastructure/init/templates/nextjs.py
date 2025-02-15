from application.init import KTemplateProtocol


class NextJSTemplate(KTemplateProtocol):
    def get_excludes(self) -> str:
        return (
            "node_modules\n"
            ".next\n"
            "out\n"
            ".env\n"
            ".git\n"
        )

    def get_includes(self) -> str:
        return (
            "*.js\n"
            "*.jsx\n"
            "*.ts\n"
            "*.tsx\n"
            "next.config.js\n"
            "package.json\n"
        )

    def get_rules(self) -> str:
        return (
	        "- Use the Official Next.js Project Structure"
	        "   - Use the app/ directory (Next.js 13+ with the App Router) or the pages/ directory (legacy approach)."
	        "   - Keep pages or route-specific files organized by URL structure (e.g., /pages/blog/[slug].jsx)."
	        "   - For the App Router, organize route segments in nested folders with necessary layout, template, and page files."
	        "- Environment Variables & Configuration"
	        "   - Store sensitive or environment-specific data in .env files and load them via Next.js environment variables."
	        "   - Never commit secrets to version control."
	        "- Components & Reusable Code"
	        "   - Place reusable UI components in a components/ directory (or similarly named folder)."
	        "   - Use clear, descriptive naming conventions for components (e.g., UserCard.jsx, NavBar.jsx)."
	        "   - Keep components small, modular, and focused on a single responsibility."
	        "- Styling & Theming"
	        "   - Choose a consistent styling approach: CSS modules, styled-components, Tailwind CSS, etc."
	        "   - Keep global styles (if any) in a dedicated file like globals.css or an equivalent in the app/ directory."
	        "   - Use a consistent naming scheme for class names, and avoid heavily nested styling when possible."
	        "- Data Fetching & API Routes"
	        "   - For the App Router, use fetch or server components for data fetching where it makes sense."
	        "   - In the Pages Router, use getStaticProps, getServerSideProps, or getStaticPaths as appropriate."
	        "   - Implement API routes under the pages/api/ (or app/api/ for Next.js 13+)."
	        "   - Ensure your API handlers handle errors and status codes consistently."
	        "- File Naming & Structure"
	        "   - Align file names with their primary export (e.g., components/Modal.jsx exports Modal)."
	        "   - Group related components under feature-specific folders if you have many components."
	        "   - Use index.js (or index.ts) for aggregator files in subfolders when it makes sense."
	        "- TypeScript (Optional)"
	        "   - If using TypeScript, place .d.ts files for type declarations in a dedicated folder like types/."
	        "   - Use strict mode in tsconfig.json for safer code."
	        "   - Keep type definitions consistent and well-documented."
	        "- Routing & Navigation"
	        "   - Use the built-in Next.js <Link> component for client-side transitions."
	        "   - Define dynamic routes using the appropriate bracket notation [param] or nested routes in app/."
	        "   - Provide fallback or catch-all routes (e.g., pages/404.js or [...slug].js) as needed."
	        "- Code Quality & Testing"
	        "   - Use ESLint with a Next.js-compatible config (e.g., eslint-config-next)."
	        "   - Auto-format code with Prettier (or another formatter) to maintain a consistent style."
	        "   - Write tests for critical pages and components (e.g., using Jest, React Testing Library, or Cypress)."
	        "   - Check for regressions and performance bottlenecks with Lighthouse or Next.js analytics."
	        "- Performance & Optimization"
	        "   - Leverage image optimization with Next.js <Image> component."
	        "   - Use lazy loading (dynamic() imports) for large, non-critical components."
	        "   - Optimize fonts with Next.js built-in font optimization or a third-party approach."
	        "   - Cache and pre-fetch data whenever possible with getStaticProps or React Query (if used)."
	        "- Deployment & CI/CD"
	        "   - Ensure environment variables are properly set in your hosting environment (Vercel, AWS, etc.)."
	        "   - Use automated pipelines to run tests and lint checks on pull requests."
	        "   - Apply code review policies to maintain quality and consistency."
	        "- Documentation"
	        "   - Maintain a clear README.md that explains project setup, scripts, and deployment steps."
	        "   - Provide usage documentation for complex components or features."
	        "   - Keep a changelog or release notes if you publish multiple versions."
        )
