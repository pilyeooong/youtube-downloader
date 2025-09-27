import json
from youtube_comment_downloader import YoutubeCommentDownloader

def download_comments(url, authors_only=False):
    """
    Download comments from a YouTube video

    Args:
        url (str): YouTube video URL
        authors_only (bool): If True, extract only comment authors
    """
    # Initialize the downloader
    downloader = YoutubeCommentDownloader()

    # Extract video ID from URL for filename
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
    else:
        print("Invalid YouTube URL format")
        return

    if authors_only:
        print(f"Downloading comment authors for video ID: {video_id}")
    else:
        print(f"Downloading comments for video ID: {video_id}")
    print("This may take a while depending on the number of comments...")

    try:
        # Download comments
        comments = downloader.get_comments_from_url(url)

        if authors_only:
            # Collect only unique authors
            unique_authors = set()
            comment_count = 0

            for comment in comments:
                author = comment.get('author', 'Unknown')
                unique_authors.add(author)
                comment_count += 1

                # Show progress every 100 comments
                if comment_count % 100 == 0:
                    print(f"Processed {comment_count} comments, found {len(unique_authors)} unique authors...")

            # Save unique authors only
            filename = f"{video_id}_unique_authors.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                for author in sorted(unique_authors):
                    f.write(f"{author}\n")

            print(f"\nTotal comments processed: {comment_count}")
            print(f"Total unique authors: {len(unique_authors)}")
            print(f"Unique authors saved to: {filename}")

            # Show sample authors
            print(f"\nSample authors (first 10):")
            for i, author in enumerate(list(unique_authors)[:10]):
                print(f"{i+1}. {author}")

        else:
            # Collect all comments (original functionality)
            all_comments = []
            comment_count = 0

            for comment in comments:
                all_comments.append(comment)
                comment_count += 1

                # Show progress every 100 comments
                if comment_count % 100 == 0:
                    print(f"Downloaded {comment_count} comments...")

            # Save to JSON file
            filename = f"{video_id}_comments.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_comments, f, ensure_ascii=False, indent=2)

            print(f"\nTotal comments downloaded: {comment_count}")
            print(f"Comments saved to: {filename}")

            # Show sample of first few comments
            if all_comments:
                print("\nSample comments:")
                for i, comment in enumerate(all_comments[:3]):
                    print(f"\n--- Comment {i+1} ---")
                    print(f"Author: {comment.get('author', 'Unknown')}")
                    print(f"Likes: {comment.get('votes', 0)}")
                    print(f"Text: {comment.get('text', '')[:200]}...")
                    if comment.get('time'):
                        print(f"Time: {comment.get('time')}")

    except Exception as e:
        print(f"Error downloading comments: {str(e)}")
        print("Please check if the URL is valid and the video has comments enabled.")

if __name__ == "__main__":
    # Get YouTube URL from user input
    url = input("Enter YouTube URL: ").strip()

    if not url:
        print("Please provide a valid YouTube URL")
        exit()

    # Ask user what they want to download
    print("\nWhat would you like to download?")
    print("1. Full comments (JSON)")
    print("2. Comment authors only (TXT)")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        download_comments(url, authors_only=False)
    elif choice == "2":
        download_comments(url, authors_only=True)
    else:
        print("Invalid choice. Please run the script again and select 1 or 2.")