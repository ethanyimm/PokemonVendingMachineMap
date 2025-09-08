#!/bin/bash

# Set project variables
PROJECT_ID="pokemon-vending-map"
REGION="us-central1"
INSTANCE_NAME="pokemon-db"
DB_NAME="vending_machine"
DB_USER="pokemon-app"

echo "🚀 Deploying Pokemon Vending Machine Map"
echo "========================================"

# 1. Set up Google Cloud project
echo "📝 Setting up Google Cloud project..."
gcloud projects create $PROJECT_ID --name="Pokemon Vending Machine Map" 2>/dev/null || echo "Project already exists"
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
echo "🔧 Enabling APIs..."
gcloud services enable run.googleapis.com
gcloud services enable sql-component.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# 3. Create Cloud SQL instance (free tier)
echo "🗄️ Creating Cloud SQL instance..."
gcloud sql instances create $INSTANCE_NAME \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=$REGION \
    --storage-type=HDD \
    --storage-size=10GB \
    --storage-auto-increase \
    --backup-start-time=03:00 \
    --enable-bin-log \
    2>/dev/null || echo "Instance already exists"

# 4. Create database
echo "📊 Creating database..."
gcloud sql databases create $DB_NAME --instance=$INSTANCE_NAME 2>/dev/null || echo "Database already exists"

# 5. Generate secure password
DB_PASSWORD=$(openssl rand -base64 32)
echo "🔐 Generated secure password for database user"

# 6. Create database user
echo "👤 Creating database user..."
gcloud sql users create $DB_USER \
    --instance=$INSTANCE_NAME \
    --password=$DB_PASSWORD \
    2>/dev/null || echo "User already exists, updating password..."
    
gcloud sql users set-password $DB_USER \
    --instance=$INSTANCE_NAME \
    --password=$DB_PASSWORD

# 7. Get connection name
CONNECTION_NAME=$(gcloud sql instances describe $INSTANCE_NAME --format="value(connectionName)")
echo "🔗 Connection name: $CONNECTION_NAME"

# 8. Deploy backend to Cloud Run
echo "🚀 Deploying backend..."
cd backend

gcloud run deploy pokemon-backend \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --add-cloudsql-instances $CONNECTION_NAME \
    --set-env-vars="DB_HOST=localhost,DB_PORT=3306,DB_USER=$DB_USER,DB_PASSWORD=$DB_PASSWORD,DB_NAME=$DB_NAME,CLOUD_SQL_CONNECTION_NAME=$CONNECTION_NAME" \
    --memory=512Mi \
    --cpu=1 \
    --timeout=300 \
    --concurrency=80 \
    --max-instances=10

# 9. Get backend URL
BACKEND_URL=$(gcloud run services describe pokemon-backend --platform managed --region $REGION --format="value(status.url)")
echo "🌐 Backend URL: $BACKEND_URL"

# 10. Export local database (you'll need to run this manually)
echo ""
echo "📋 Next steps:"
echo "1. Export your local database:"
echo "   mysqldump -u root -p vending_machine > vending_machine_backup.sql"
echo ""
echo "2. Upload to Cloud Storage bucket and import:"
echo "   gsutil mb gs://$PROJECT_ID-db-backups"
echo "   gsutil cp vending_machine_backup.sql gs://$PROJECT_ID-db-backups/"
echo "   gcloud sql import sql $INSTANCE_NAME gs://$PROJECT_ID-db-backups/vending_machine_backup.sql --database=$DB_NAME"
echo ""
echo "3. Update your frontend to use: $BACKEND_URL"
echo "4. Deploy frontend with Firebase Hosting"
echo ""
echo "✅ Deployment complete!"
echo "Database Password: $DB_PASSWORD (save this securely!)"