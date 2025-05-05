# Eco-Mood Travel Frontend

This is the frontend application for the Eco-Mood Travel Planner, a web application that generates emotion-driven itineraries by analyzing traveler reviews.

## Features

- User authentication (login, registration, profile management)
- Interactive map with emotion-based heatmaps
- Review analysis and visualization
- Itinerary builder with drag-and-drop functionality
- Responsive design with Tailwind CSS

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn

## Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

## Development

To start the development server:

```bash
npm start
# or
yarn start
```

The application will be available at `http://localhost:3000`.

## Building for Production

To create a production build:

```bash
npm run build
# or
yarn build
```

The build artifacts will be stored in the `build/` directory.

## Project Structure

```
src/
  ├── components/     # React components
  ├── contexts/       # React contexts (auth, etc.)
  ├── services/       # API services
  ├── styles/         # CSS and Tailwind styles
  ├── types/          # TypeScript type definitions
  ├── App.tsx         # Main application component
  └── index.tsx      # Application entry point
```

## Technologies Used

- React 18
- TypeScript
- React Router v6
- Axios
- Leaflet
- Tailwind CSS
- PostCSS

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 