# WebClassify: Intelligent Web Content Analyzer

WebClassify is a system that scrapes websites, classifies their content, stores vector representations, and provides similarity search functionality.

## Features

- Web scraping API
- Website classification using zero-shot learning
- Vector storage and similarity search using Qdrant
- Dockerized application for easy deployment

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/webclassify.git
   cd webclassify
   ```

2. Build the Docker image:
   ```
   docker build -t webclassify .
   ```

3. Run the Docker container:
   ```
   docker run -p 8000:8000 webclassify
   ```

The application will be available at `http://localhost:8000`.

## Usage Examples

1. Scrape and classify a website:
   ```
   curl -X POST "http://localhost:8000/scrape" -H "Content-Type: application/json" -d '{"urls": ["https://example.com"]}'
   ```

2. Search for similar content:
   ```
   curl -X POST "http://localhost:8000/search" -H "Content-Type: application/json" -d '{"text": "Latest news updates"}'
   ```

## Approach and Assumptions

- We use FastAPI for creating the API endpoints due to its high performance and ease of use.
- BeautifulSoup is used for web scraping, assuming most websites have a standard HTML structure.
- The zero-shot classification model (valhalla/distilbart-mnli-12-1) is used for website categorization, assuming it can generalize well to various website types.
- Qdrant is chosen as the vector database for its performance and ease of integration.
- We assume that the input URLs are valid and accessible.

## Future Improvements

- Implement caching to avoid re-scraping recently processed websites.
- Add more comprehensive error handling and logging.
- Implement rate limiting for the web scraping functionality.
- Expand the classification categories and fine-tune the model for better accuracy.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
