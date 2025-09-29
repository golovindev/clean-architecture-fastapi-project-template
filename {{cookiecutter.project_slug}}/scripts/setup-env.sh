#!/bin/bash

# Setup environment variables from template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp env.template .env
    echo "✅ .env file created successfully!"
    echo "📝 Please review and modify .env file if needed"
else
    echo "⚠️  .env file already exists, skipping creation"
    echo "📝 If you want to update from template, run: cp env.template .env"
fi
