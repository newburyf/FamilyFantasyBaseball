# About
Custom playoff fantasy baseball with my family.

Sets up a local sqlite database to store data and displayed up to date data on a static GitHub pages site.

There are so many changes that I could make but it works for what it is, in future years I may look to make improvements.

# Related Documentation
[Stats API Python wrapper](https://github.com/toddrob99/MLB-StatsAPI/wiki)

[Official MLB Stats API Docs](https://github.com/MajorLeagueBaseball/google-cloud-mlb-hackathon/tree/main/datasets/mlb-statsapi-docs)

[Python sqlite3 docs](https://docs.python.org/3/library/sqlite3.html)

# Future Improvements

### Shorter Term

- User Interaction:
    - Require year entry only once on CLI startup
    - Streamline drafting
        - Remove need to have added player to DB first
        - Make player/team selection easier
        - Allow for draft continuations from previous rounds
- Clean up CLI code
    - Make getting user input cleaner
- Better exception handling
- Allow for different scoring schemes
- Allow for partial stats updates (not all games finished)
- Make website look nicer

### Longer Term
- Actually have a web server instead of just a static website
- Remove need to manually start stat collection
- Add drafting functionality to website
- Allow for editing/viewing data through CLI/website

