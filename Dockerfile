
# Use Node.js Alpine image for smaller footprint
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Install a simple HTTP server
RUN npm install -g serve

# Expose port
EXPOSE 8080

# Start the application
CMD ["serve", "-s", "dist", "-l", "8080"]
