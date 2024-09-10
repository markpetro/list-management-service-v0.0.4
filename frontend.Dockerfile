# frontend.Dockerfile
# Use a node image as the base image to compile the application
FROM node:16-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY frontend/package.json .
COPY frontend/package-lock.json .

# Install dependencies
RUN npm install

# Copy all files to the working directory
COPY frontend .

# Build the application
RUN npm run build

# Use an nginx image to serve the static files
FROM nginx:alpine

# Copy the built files from the previous stage to the nginx html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]