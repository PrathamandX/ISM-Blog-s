import asyncio
from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx
from sqlalchemy import delete, select, update

import models
from config import settings
from database import AsyncSessionLocal, engine
from image_utils import _get_s3_client
from main import app

POPULATE_IMAGES_DIR = Path("populate_images")

USERS = [
    {
        "username": "Pratham",
        "email": "CoreyMSchafer@gmail.com",
        "password": "TestPassword1!",
        "image": "img1.jpeg",
    },
    {
        "username": "Prathamesh",
        "email": "TestEmail2@test.com",
        "password": "TestPassword2!",
        # No image - uses default
    },
    {
        "username": "Renu",
        "email": "TestEmail3@test.com",
        "password": "TestPassword3!",
        "image": "img2.jpeg",
    },
    {
        "username": "Shubh",
        "email": "TestEmail4@test.com",
        "password": "TestPassword4!",
        "image": "img3.jpeg",
    },
    {
        "username": "Aj",
        "email": "TestEmail5@test.com",
        "password": "TestPassword5!",
        "image": "img4.jpeg",
    },
    {
        "username": "AJj",
        "email": "TestEmail6@test.com",
        "password": "TestPassword6!",
        "image": "img5.jpeg",
    },
]

POSTS = [
{
"title": "The Joy of Morning Walks",
"content": "A simple morning walk can clear your mind, improve your mood, and set a positive tone for the rest of the day. It's one of the easiest habits to build."
},
{
"title": "Why I Started Reading Again",
"content": "After years of scrolling through social media, I decided to pick up books again. The difference in focus and mental clarity has been remarkable."
},
{
"title": "Coffee Shops as Workspaces",
"content": "There's something about the background chatter and aroma of coffee that makes working in a café surprisingly productive."
},
{
"title": "Learning a New Language",
"content": "Even fifteen minutes a day can make a noticeable difference when learning a language. Consistency beats intensity every time."
},
{
"title": "The Power of Small Habits",
"content": "Tiny improvements repeated daily often lead to bigger results than occasional bursts of motivation."
},
{
"title": "Why Hydration Matters",
"content": "Most people underestimate how much water affects energy levels, concentration, and overall well-being."
},
{
"title": "My Favorite Productivity Trick",
"content": "Breaking large tasks into smaller, manageable pieces makes even the most intimidating projects feel achievable."
},
{
"title": "A Weekend Without Screens",
"content": "Spending a weekend away from devices revealed how often I reach for my phone without thinking."
},
{
"title": "The Beauty of Local Travel",
"content": "You don't always need a plane ticket to have an adventure. Exploring nearby places can be surprisingly rewarding."
},
{
"title": "Cooking at Home More Often",
"content": "Preparing meals yourself not only saves money but also helps you appreciate ingredients and flavors more deeply."
},
{
"title": "The First Time I Tried Camping",
"content": "Sleeping under the stars and waking up to nature's sounds was both challenging and refreshing."
},
{
"title": "How Music Shapes My Day",
"content": "Different playlists help me focus, relax, exercise, and even spark creativity when I'm stuck."
},
{
"title": "The Importance of Good Sleep",
"content": "No productivity hack can replace a proper night's sleep. Everything works better when you're well-rested."
},
{
"title": "Trying a New Hobby",
"content": "Stepping outside your comfort zone and learning something unfamiliar can reignite curiosity and excitement."
},
{
"title": "Digital Notes vs Paper Notes",
"content": "Each method has advantages, but combining both often provides the best balance between convenience and retention."
},
{
"title": "The Art of Saying No",
"content": "Protecting your time often means declining opportunities that don't align with your priorities."
},
{
"title": "A Beginner's Guide to Journaling",
"content": "Writing down thoughts regularly can help organize ideas, process emotions, and track personal growth."
},
{
"title": "What I Learned From Failure",
"content": "Mistakes are rarely enjoyable, but they often provide the most valuable lessons."
},
{
"title": "Exploring Street Food",
"content": "Some of the best meals I've ever had came from small stalls and local vendors rather than expensive restaurants."
},
{
"title": "The Benefits of Strength Training",
"content": "Strength training improves more than muscles; it builds confidence, discipline, and resilience."
},
{
"title": "Why Curiosity Is a Superpower",
"content": "Asking questions and seeking understanding often opens doors that expertise alone cannot."
},
{
"title": "Working Remotely: The Good and Bad",
"content": "Remote work offers flexibility but requires intentional effort to maintain structure and connection."
},
{
"title": "My Favorite Travel Memory",
"content": "Sometimes the unexpected moments become the stories we remember years later."
},
{
"title": "The Challenge of Minimalism",
"content": "Owning less can simplify life, but deciding what truly matters is often harder than expected."
},
{
"title": "Why I Started Exercising Regularly",
"content": "The physical benefits are obvious, but the mental benefits turned out to be even more valuable."
},
{
"title": "Finding Focus in a Distracted World",
"content": "Notifications, emails, and endless feeds compete for attention. Creating boundaries makes a huge difference."
},
{
"title": "The Magic of Libraries",
"content": "Libraries remain one of the most underrated resources for learning, exploration, and quiet reflection."
},
{
"title": "My First Coding Project",
"content": "It wasn't impressive, but seeing something work because of code I wrote felt incredibly rewarding."
},
{
"title": "The Value of Patience",
"content": "Many worthwhile goals take longer than expected. Patience helps bridge the gap between effort and results."
},
{
"title": "A Rainy Day Reflection",
"content": "Sometimes slowing down and watching the rain can provide a welcome pause from a busy schedule."
},
{
"title": "Why People Love Puzzles",
"content": "Puzzles challenge the mind while offering a satisfying sense of progress and accomplishment."
},
{
"title": "The Benefits of Walking Meetings",
"content": "Combining movement with conversation can spark creativity and improve engagement."
},
{
"title": "Learning From Different Cultures",
"content": "Exposure to new perspectives often broadens understanding and challenges assumptions."
},
{
"title": "The Science of Motivation",
"content": "Motivation comes and goes, but systems and habits provide a more reliable path to progress."
},
{
"title": "Trying New Foods",
"content": "Every unfamiliar dish offers a chance to discover flavors and traditions from around the world."
},
{
"title": "How Technology Changed Daily Life",
"content": "Many conveniences we take for granted today would have seemed extraordinary just a few decades ago."
},
{
"title": "The Benefits of Team Sports",
"content": "Team sports teach cooperation, communication, and perseverance alongside physical fitness."
},
{
"title": "A Love Letter to Bookstores",
"content": "Browsing shelves and discovering unexpected books remains a uniquely enjoyable experience."
},
{
"title": "The Importance of Lifelong Learning",
"content": "The world changes constantly, and continuing to learn helps us adapt and grow."
},
{
"title": "Why Nature Inspires Creativity",
"content": "Stepping away from screens and spending time outdoors often leads to fresh ideas."
},
{
"title": "The Joy of Helping Others",
"content": "Small acts of kindness can create meaningful connections and improve both lives involved."
},
{
"title": "Managing Stress Effectively",
"content": "Healthy routines, exercise, and perspective can make challenging situations more manageable."
},
{
"title": "Lessons From Traveling Alone",
"content": "Solo travel encourages independence, adaptability, and confidence in unfamiliar situations."
}
]


# The 44th post - always the oldest (easter egg for pagination tutorial)
POST_44 = {
    "title": "The First Post",
    "content": "This will always be the first post.",
}


async def clear_existing_data() -> None:
    # Delete profile pictures from S3 (need DB records to know which files)
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(models.User.image_file).where(models.User.image_file.is_not(None)),
        )
        filenames = result.scalars().all()

    if filenames:
        s3 = _get_s3_client()
        s3.delete_objects(
            Bucket=settings.s3_bucket_name,
            Delete={"Objects": [{"Key": f"profile_pics/{f}"} for f in filenames]},
        )
        print(f"Deleted {len(filenames)} images from S3")

    # Clear database tables (order respects foreign keys)
    async with AsyncSessionLocal() as db:
        await db.execute(delete(models.PasswordResetToken))
        await db.execute(delete(models.Post))
        await db.execute(delete(models.User))
        await db.commit()
    print("Cleared existing data")


async def update_post_dates() -> None:
    now = datetime.now(UTC)

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(models.Post).order_by(models.Post.id))
        posts = result.scalars().all()

        if not posts:
            return

        # First post (POST_44) is the oldest - ~90 days ago
        await db.execute(
            update(models.Post)
            .where(models.Post.id == posts[0].id)
            .values(date_posted=now - timedelta(days=90)),
        )

        # Remaining posts: each ~1.5 days newer than previous
        for i, post in enumerate(posts[1:], start=1):
            days_ago = (len(posts) - i) * 1.5
            hours_offset = (i * 7) % 24
            post_date = now - timedelta(days=days_ago, hours=hours_offset)
            await db.execute(
                update(models.Post)
                .where(models.Post.id == post.id)
                .values(date_posted=post_date),
            )

        await db.commit()
    print("Updated post dates")


async def populate() -> None:
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://localhost",
    ) as client:
        # Clear existing data (S3 images first, then database)
        await clear_existing_data()

        users: list[dict] = []

        print(f"\nCreating {len(USERS)} users...")
        for user_data in USERS:
            response = await client.post(
                "/api/users",
                json={
                    "username": user_data["username"],
                    "email": user_data["email"],
                    "password": user_data["password"],
                },
            )
            response.raise_for_status()
            user = response.json()
            print(f"  Created: {user['username']}")

            response = await client.post(
                "/api/users/token",
                data={
                    "username": user_data["email"],
                    "password": user_data["password"],
                },
            )
            response.raise_for_status()
            token = response.json()["access_token"]

            if image_name := user_data.get("image"):
                image_path = POPULATE_IMAGES_DIR / image_name
                if image_path.exists():
                    response = await client.patch(
                        f"/api/users/{user['id']}/picture",
                        files={
                            "file": (
                                image_name,
                                image_path.read_bytes(),
                                "image/png",
                            ),
                        },
                        headers={"Authorization": f"Bearer {token}"},
                    )
                    response.raise_for_status()
                    print(f"    Uploaded: {image_name}")

            users.append(
                {"id": user["id"], "username": user["username"], "token": token},
            )

        print(f"\nCreating {len(POSTS) + 1} posts...")

        # First create POST_44 (will become oldest after date update)
        response = await client.post(
            "/api/posts",
            json={"title": POST_44["title"], "content": POST_44["content"]},
            headers={"Authorization": f"Bearer {users[0]['token']}"},
        )
        response.raise_for_status()
        print(f"  Created: '{POST_44['title']}'")

        # Create remaining posts in reverse (last in list = oldest, first = newest)
        for i, post_data in enumerate(reversed(POSTS)):
            user = users[i % len(users)]
            response = await client.post(
                "/api/posts",
                json={
                    "title": post_data["title"],
                    "content": post_data["content"],
                },
                headers={"Authorization": f"Bearer {user['token']}"},
            )
            response.raise_for_status()
            title = post_data["title"]
            print(
                f"  Created: '{title[:50]}...'"
                if len(title) > 50
                else f"  Created: '{title}'",
            )

        print("\nUpdating post dates...")
        await update_post_dates()

    await engine.dispose()

    print("\nDone!")
    print(f"  {len(USERS)} users")
    print(f"  {len(POSTS) + 1} posts")
    print("  Profile pictures uploaded to S3")


if __name__ == "__main__":
    asyncio.run(populate())