# Build and production stage
FROM node:20-alpine

WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including dev) for building
RUN npm install

# Copy env file
COPY .env.docker .env.local

# Copy all project files
COPY . .

# Build the Next.js app
RUN npm run build

# Remove dev dependencies
RUN npm prune --production

EXPOSE 3000

# Start the production server
CMD ["npm", "start"]
