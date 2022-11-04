#!/bin/bash
set -e

# Constants
VERSION=$1
PACKAGE_NAME="trading-view-images-downloader-$VERSION.tar.gz"
APP_PACKAGE_FOLDER="dist"
APP_FOLDER="$HOME/App/trading-view-images-downloader"

echo "Start deploy app: $PACKAGE_NAME to $APP_FOLDER"
rm -rf "$APP_FOLDER/trading-view-images-downloader-$VERSION"
mkdir -p $APP_FOLDER
cp "$APP_PACKAGE_FOLDER/$PACKAGE_NAME" "$APP_FOLDER"
cd "$APP_FOLDER" || exit 1
tar -xvzf "$PACKAGE_NAME"
echo "Finished deploy app"