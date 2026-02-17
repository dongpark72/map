FROM nginx:alpine

# Copy nginx configuration
COPY nginx_custom.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
