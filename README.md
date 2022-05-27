# BergOnline

VIDEO: https://youtu.be/4d1oBijKjCM

Welcome to BergOnline! To begin using BergOnline, the first step is to manually run the command "python parse.py" in the /bergonline folder. This may take a while, ~2 or 3 minutes. This code scrapes the HUDS database at the time you run the code, loads it into a SQL database, and accordingly updates the website. We encourage running this code so that the website is useful, but the website works without it as well (it would just show old data). The code should print "meal0loaded" when breakfast is loaded, "meal1loaded" for lunch, and "meal2loaded" for dinner, at which point the data is fully loaded and the website is ready for use.

Next, run "flask run" and open the website. You should be redirected to the login page. Since you do not have a login yet, feel free to register yourself by clicking the "Register" link under the login form. This will take you to the register form. Register by inputting a username, a password, and the same password for the confirmation. You can test the functionality by:
- not inputting a username
- not inputting a password
- not inputting a confirmation
- not having the password and confirmation match
- inputting a username already in the database, i.e. "thisisatest".

Now you are at the main screen. You can test the logout button on the top right, which takes you to the login screen. Input your login information to get back in. Again, you can test the functionality by not inputting a username, not inputting a password, inputting an incorrect username, or inputting an incorrect password corresponding to a username.

Time to use BergOnline now! On the main screen, you can see all the menu items of the day you are viewing this on. This includes the name of the menu item, the meal number (1 - breakfast, 2 - lunch, 3 - dinner), and a number of nutrition data values. To see these in more detail, we use the Nutrition tab. Click that tab and input any of the menu items from the original page (this is NOT case sensitive, so you can have a name such as "ChObanI NONfat PLAin GreEk yOGurt" or "WAFfleS"), and you should see the nutrition data of that specific item. Test out not putting in any value. An item such as hummus appears in both lunch and dinner, but if you input "Hummus", you will see we specifically engineered the website to only return one row to avoid repeating nutrition data. Test out an invalid menu item, for example "Umbrella". Nothing will show up in the table in the resulting html file, since the code did not find anything.

Now, go to "What People are Eating". This will be a database where people using BergOnline can add what they are eating. As you can see, there are some items already in the database, like 3 servings of congee or 1 serving of a muffin. Go to "Input Meal" to input your own data. Test out one serving of a menu item, such as "Sambal Sauce" or "Sliced Tomatoes". You can go to "What People are Eating" and see it update. Now, go back to "Input Meal" and input multiple servings of any menu item. Go back to the "What People are Eating" tab and look at the row which corresponds to that input. You should see that the calories, fat, and other nutritional values are multiplied by however many servings you inputted. Test out not inputting anything, inputting an invalid menu item like "Umbrella", or a noninteger servings amount. 

NOTE: If nothing shows up when you believe it should, it may be a typo on HUDS' part. For example, "Farro with Asparagus, Peas" does not return anything, but "Farro with  Asparagus, Peas" does (two spaces between with and Asparagus).

Now, go to "See a Meal". This will show a table of the menu items you input separated by commas. Try out a comma-separated list of menu items, like "Waffles, Sambal Sauce, Sliced Tomatoes". You should see a table of these menu items with the nutrition data. An item such as hummus appears in both lunch and dinner, but if you input "Hummus", you will see we specifically engineered the website to only return one row to avoid repeating nutrition data. Test out an invalid menu item in the list, for example "Umbrella". Nothing will show up for "Umbrella" in the table in the resulting html file, since the code did not find anything. Test out not inputting anything.

Finally, go to "Discussion". This is a discussion board which is a database of posts about the food at Annenberg. Now go to "Post". You can post posts about the food in Annenberg and see others' posts in a discussion board as well. Test out posting anything you want and go back to "Discussion" to see that it works. Test out not inputting anything.

That's BergOnline!

