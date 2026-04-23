import datetime
import random

all_themes = [
    "default",
    "cerulean",
    "cosmo",
    "cyborg",
    "darkly",
    "flatly",
    "journal",
    "litera",
    "lumen",
    "lux",
    "materia",
    "minty",
    "pulse",
    "sandstone",
    "simplex",
    "sketchy",
    "slate",
    "solar",
    "spacelab",
    "superhero",
    "united",
    "yeti",
    "brite",
    "raya",
    "morph",
    "quartz",
    "vapor",
    "zephyr",
]


def build_sample_db(db, User, Page, Organization, Social):
    """
    Populate a small db with some example entries.
    This version creates multiple organizations and randomly assigns them to users.
    """

    # Drop all existing tables and recreate them from the models
    db.drop_all()
    db.create_all()

    # Define the data for multiple dummy organizations
    organizations_data = [
        {"name": "ACME Corporation", "shortname": "ACME"},
        {"name": "Stark Industries", "shortname": "Stark"},
        {"name": "Wayne Enterprises", "shortname": "Wayne"},
        {"name": "Globex Corporation", "shortname": "Globex"},
        {"name": "Cyberdyne Systems", "shortname": "Cyberdyne"},
    ]

    # This list will hold the created Organization objects
    organizations = []

    # Create Organization objects and add them to the database
    for org_data in organizations_data:
        organization = Organization(
            name=org_data["name"], shortname=org_data["shortname"]
        )
        db.session.add(organization)
        organizations.append(organization)

    # Sample data for creating users
    first_names = [
        "Harry",
        "Amelia",
        "Oliver",
        "Jack",
        "Isabella",
        "Charlie",
        "Sophie",
        "Mia",
        "Jacob",
        "Thomas",
        "Emily",
        "Lily",
        "Ava",
        "Isla",
        "Alfie",
        "Olivia",
        "Jessica",
        "Riley",
        "William",
        "James",
        "Geoffrey",
        "Lisa",
        "Benjamin",
        "Stacey",
        "Lucy",
    ]
    last_names = [
        "Brown",
        "Smith",
        "Patel",
        "Jones",
        "Williams",
        "Johnson",
        "Taylor",
        "Thomas",
        "Roberts",
        "Khan",
        "Lewis",
        "Jackson",
        "Clarke",
        "James",
        "Phillips",
        "Wilson",
        "Ali",
        "Mason",
        "Mitchell",
        "Rose",
        "Davis",
        "Davies",
        "Rodriguez",
        "Cox",
        "Alexander",
    ]

    # Create users and assign a random organization to each one
    for i in range(len(first_names)):
        user = User()
        user.name = f"{first_names[i]} {last_names[i]}"
        user.email = f"{first_names[i].lower()}@example.com"
        user.dob = (
            datetime.date(
                random.randint(1980, 2010), random.randint(1, 12), random.randint(1, 28)
            )
            if random.choices([True, False], weights=[0.8, 0.2])[0]
            else None
        )  # Randomly assign
        user.social = (
            random.choice(list(Social))
            if random.choices([True, False], weights=[0.8, 0.2])[0]
            else None
        )  # Randomly assign

        # Pick a random organization from the list created above
        user.organization = random.choice(organizations)
        user.daily_reminder = (
            datetime.time(random.randint(0, 23), random.randint(10, 20))
            if random.choices([True, False], weights=[0.8, 0.2])[0]
            else None
        )  # Randomly assign

        db.session.add(user)

    # Sample data for creating pages
    sample_text = [
        {
            "title": "de Finibus Bonorum et Malorum - Part I",
            "content": (
                "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do "
                "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim "
                "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut "
                "aliquip ex ea commodo consequat. Duis aute irure dolor in "
                "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
                "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
                "culpa qui officia deserunt mollit anim id est laborum."
            ),
        },
        {
            "title": "de Finibus Bonorum et Malorum - Part II",
            "content": (
                "Sed ut perspiciatis unde omnis iste natus error sit voluptatem "
                "accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae "
                "ab illo inventore veritatis et quasi architecto beatae vitae dicta "
                "sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit "
                "aspernatur aut odit aut fugit, sed quia consequuntur magni dolores "
                "eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, "
                "qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, "
                "sed quia non numquam eius modi tempora incidunt ut labore et dolore "
                "magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis "
                "nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut "
                "aliquid ex ea commodi consequatur? Quis autem vel eum iure "
                "reprehenderit qui in ea voluptate velit esse quam nihil molestiae "
                "consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla "
                "pariatur?"
            ),
        },
        {
            "title": "de Finibus Bonorum et Malorum - Part III",
            "content": (
                "At vero eos et accusamus et iusto odio dignissimos ducimus qui "
                "blanditiis praesentium voluptatum deleniti atque corrupti quos "
                "dolores et quas molestias excepturi sint occaecati cupiditate non "
                "provident, similique sunt in culpa qui officia deserunt mollitia "
                "animi, id est laborum et dolorum fuga. Et harum quidem rerum "
                "facilis est et expedita distinctio. Nam libero tempore, cum soluta "
                "nobis est eligendi optio cumque nihil impedit quo minus id quod "
                "maxime placeat facere possimus, omnis voluptas assumenda est, omnis "
                "dolor repellendus. Temporibus autem quibusdam et aut officiis debitis "
                "aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae "
                "sint et molestiae non recusandae. Itaque earum rerum hic tenetur a "
                "sapiente delectus, ut aut reiciendis voluptatibus maiores alias "
                "consequatur aut perferendis doloribus asperiores repellat."
            ),
        },
    ]

    # Create Page objects and add them to the database
    for entry in sample_text:
        page = Page()
        page.title = entry["title"]
        page.content = entry["content"]
        db.session.add(page)

    # Commit all the changes to the database
    db.session.commit()
    return
