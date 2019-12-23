<h1>Purpose</h1>
<p>Sparkify needs to know activity of user to gain insight of how to better service user.<br>
By creating this database, user activities can be retrieve easily and quickly by selecting only needed data<br>
or join only necessary data to be use in analysis step</p>
<p>One of the goal of analyzing user data is to find what song user listening to which can be used for recommendation system or creating top chart by data gathered by Sparkify.</p>
<h1>Fact Table</h1>
<p> songplays table with songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent<br>
    as an data in column<p>
<p> songplay Fact Table enables analysis team to know essential information for each song that being played.<br>
    It can be used to analysis song that often played in specific period of time or specific location as an example of analysis.<p>
<h1>dimension table</h1>
<p>users - users in the app, this table is used for gaining additional information from user in case needed</p>
<p>songs - songs in music database,this table is used for gaining additional information from each song in case needed</p>
<p>artists - artists in music database,this table is used for gaining additional information from a artist in case needed</p>
<p>time - timestamps of records in songplays broken down into specific units,this table is used for gaining insight of time that music played</p>
<p>In this schema analytics team is able to have essential data from songplays table.However, if data in songplays table is not sufficient, analytics team have an option to use data from songplays table to retrieve additional data from other dimension table.<br>
By design schema in this way, there is no redundant data which will not be used are being retrieve from fact table<p>