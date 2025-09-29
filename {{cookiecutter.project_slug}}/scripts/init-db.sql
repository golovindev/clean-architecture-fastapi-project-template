-- Database initialization script for Antiques application
-- This script runs when the PostgreSQL container starts for the first time

-- Create the main user
CREATE USER antiques_user WITH PASSWORD 'antiques_password';

-- Create the database
CREATE DATABASE antiques OWNER antiques_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE antiques TO antiques_user;

-- Connect to the antiques database
\c antiques;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'UTC';

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO antiques_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO antiques_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO antiques_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO antiques_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO antiques_user;
