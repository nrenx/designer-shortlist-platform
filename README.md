
# Project Name: Full Stack Assignment

## Objective

This project is a mobile-responsive web application that lists active interior designers from the EmptyCup platform. The application features a clean, modern interface that allows users to browse interior designers, shortlist their favorites, and interact with various filtering and sorting options. The design is based on a Figma mockup and implements both frontend functionality and backend API integration capabilities.

## Technologies Used

### Frontend
- **React** with TypeScript for component-based architecture
- **Tailwind CSS** for responsive styling and mobile-first design
- **Shadcn/ui** for consistent UI components
- **Lucide React** for modern icons
- **Mobile-responsive design** optimized for mobile devices
- **Figma reference** for pixel-perfect design implementation

### Backend
- **Static JSON** data source (ready for Flask API integration)
- **RESTful API structure** prepared for future Flask implementation
- **Docker** containerization for local development

### Development & Deployment
- **Docker** with docker-compose for local development setup
- **Vite** for fast development and building
- **TypeScript** for type safety and better development experience

## Features

### Core Functionality
- **Designer Listings**: Browse interior designers with detailed information
- **Shortlisting**: Toggle shortlist status for favorite designers
- **Filtering**: View all designers or only shortlisted ones
- **Sorting**: Sort by experience, price, or number of projects
- **Hide/Show**: Hide designers with undo functionality

### Interactive Features
- **Schedule Button**: Shows upcoming booking functionality modal
- **Gallery Button**: Displays sample portfolio images
- **Map Button**: Shows location services placeholder
- **Details Modal**: Full designer information with contact details
- **Report System**: Report inappropriate content with form submission

### Mobile-Responsive Design
- Optimized for mobile devices (320px to 480px)
- Touch-friendly interfaces
- Responsive grid layouts
- Mobile-first approach

## Project Structure

```
src/
├── components/
│   ├── ui/                 # Shadcn UI components
│   └── DesignerDirectory.tsx # Main application component
├── data/
│   └── listings.json       # Designer data (API simulation)
├── pages/
│   └── Index.tsx           # Main page component
├── hooks/
│   └── use-toast.ts        # Toast notification hook
└── lib/
    └── utils.ts            # Utility functions
```

## Setup Instructions

### Prerequisites
- Node.js (v18 or higher)
- Docker and Docker Compose
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd full-stack-assignment
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:8080`

### Docker Development Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: `http://localhost:8080`
   - The app will hot-reload when you make changes to the code

3. **Stop the application**
   ```bash
   docker-compose down
   ```

## Docker Configuration

### Dockerfile
The project includes a Dockerfile that:
- Uses Node.js Alpine image for small footprint
- Installs dependencies
- Builds the application
- Serves using a simple HTTP server

### docker-compose.yml
Orchestrates the application services:
- **Frontend service**: Runs the React application
- **Volume mounting**: Enables hot-reload during development
- **Port mapping**: Exposes the app on port 8080

## API Integration (Future Enhancement)

The application is designed to easily integrate with a Flask REST API. The current implementation uses a static JSON file (`src/data/listings.json`) that can be replaced with API calls.

### Expected API Endpoints
```
GET /api/designers          # Fetch all designers
GET /api/designers/:id      # Fetch specific designer
POST /api/designers/:id/shortlist  # Toggle shortlist
POST /api/designers/:id/report     # Report designer
```

### Flask API Setup (Future)
1. Create a Flask application with the above endpoints
2. Replace the static JSON loading with fetch calls to your API
3. Update the Docker Compose file to include the Flask service
4. Configure environment variables for API base URL

## Deployment Instructions

### Frontend Deployment (Netlify)

1. **Build the project**
   ```bash
   npm run build
   ```

2. **Deploy to Netlify**
   - Connect your GitHub repository to Netlify
   - Set build command: `npm run build`
   - Set publish directory: `dist`
   - Deploy the site

3. **Environment Variables**
   - Add any necessary environment variables in Netlify dashboard
   - Configure API base URL for production

### Backend Deployment (Cloud VM)

1. **Prepare the Flask API**
   - Create a Flask application with required endpoints
   - Containerize using Docker
   - Set up database connections

2. **Deploy to Cloud VM**
   - Use services like DigitalOcean, AWS EC2, or Google Cloud
   - Set up Docker on the VM
   - Deploy using docker-compose
   - Configure reverse proxy (nginx) for production

3. **Environment Variables**
   ```bash
   export DATABASE_URL=your_database_url
   export SECRET_KEY=your_secret_key
   export FLASK_ENV=production
   ```

## Configuration Settings

### Environment Variables
Create a `.env` file for local development:
```
VITE_API_BASE_URL=http://localhost:5000/api
VITE_ENVIRONMENT=development
```

### Production Environment
```
VITE_API_BASE_URL=https://your-api-domain.com/api
VITE_ENVIRONMENT=production
```

## Development Guidelines

### Code Style
- Use TypeScript for all new components
- Follow React best practices with hooks
- Use Tailwind CSS for styling
- Implement responsive design first

### Component Structure
- Keep components small and focused
- Use custom hooks for complex logic
- Implement proper error handling
- Add loading states for async operations

### Testing
```bash
npm run test          # Run unit tests
npm run test:watch    # Run tests in watch mode
npm run test:coverage # Generate coverage report
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   lsof -ti:8080 | xargs kill -9
   ```

2. **Docker build issues**
   ```bash
   docker system prune -a
   docker-compose build --no-cache
   ```

3. **Node modules issues**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

### Performance Optimization
- Images are loaded from Unsplash with optimized sizes
- Components use React.memo where appropriate
- Debounced search and filtering
- Lazy loading for modals and heavy components

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is created as part of an internship assignment for EmptyCup platform.

---

**Note**: This application demonstrates modern web development practices with React, TypeScript, and responsive design. The codebase is structured to be easily maintainable and scalable for future enhancements.
