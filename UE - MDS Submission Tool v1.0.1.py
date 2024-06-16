#!/usr/bin/env python
# coding: utf-8

# #### Imports

# In[1]:


import pandas as pd
import warnings
import re
import math
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
from datetime import timedelta
import openpyxl
import customtkinter as ctk
from customtkinter import *
from CTkScrollableDropdown import *
import time

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  # default='warn'
warnings.simplefilter(action='ignore', category=FutureWarning)


# ## UE App Class

# In[2]:


print("Loading")
# ================================================== UE APP ================================================== #

class UEApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.geometry("1400x800")
        self.frames = {}

        
        for F in (First, Reserves, Youths):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(First)
        self.title("Ultimate Europe - Entirely Unofficial Companion")
       
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# ======================================================================================================================= #
# ================================================== SUBMIT FIRST TEAM ================================================== #
# ======================================================================================================================= #
    
    def submit_first_team(self, players, positions, tactics, roles, roles_df, ticks, training, actions, names, password, formation, message, SPS, subs):
        driver = webdriver.Firefox() # open firefox
        driver.maximize_window() # full screen
        driver.get("http://www.ultimate-europe.co.uk/mds_form.htm") # get the web address

        #=========== Get/Enter MDS details ===========#
        turn_data = pd.read_csv("Turn Data/Turn Data.csv")
        duedate = turn_data.Deadline.squeeze()
        team_id = turn_data.TeamID.squeeze()
        team = turn_data.Team.squeeze()
        mgr = turn_data.Manager.squeeze()
        email = turn_data.Email.squeeze()
        game = turn_data.Game.squeeze()
        turn = turn_data.Turn.squeeze()
        season = turn_data.Season.squeeze()
        
        # append mds details
        driver.find_element(By.NAME, "email").send_keys(email) #email
        driver.find_element(By.NAME, "deadline").send_keys(duedate) #deadline
        driver.find_element(By.NAME, "id").send_keys(team_id) #teamid
        driver.find_element(By.NAME, "team").send_keys(team) #teamname
        driver.find_element(By.NAME, "manager").send_keys(mgr) #manager name
        driver.find_element(By.NAME, "game").send_keys(int(game)) #game number
        driver.find_element(By.NAME, "season").send_keys(int(season)) #season number
        driver.find_element(By.NAME, "turn").send_keys(int(turn)) # turn number

        file = "Turn Data/Show Team.xlsx"
        gks = pd.read_excel(open(file,"rb"), sheet_name="gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="att")
        DFA = pd.concat([deff,mid,att])

        #--------------------------- Goalkeepers --------------------------#
        PL1 = gks.query('Name == "'+ players[0] +'"'); 
        PL1_id = PL1.iloc[:,1:2].squeeze(); PL1_name = PL1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code").send_keys(PL1_id); driver.find_element(By.NAME, "surname").send_keys(PL1_name);
        
        #--------------------------- Defenders --------------------------#
        PL2 = deff.query('Name == "'+ players[1] +'"'); 
        PL2_id = PL2.iloc[:,1:2].squeeze(); PL2_name = PL2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code2").send_keys(PL2_id); driver.find_element(By.NAME, "surname2").send_keys(PL2_name); driver.find_element(By.NAME, "position2").send_keys(positions[0])

        PL3 = deff.query('Name == "'+ players[2] +'"');          # query deff on tkinter input for player 3
        PL3_Pos = "CB"; PL3_id = PL3.iloc[:,1:2].squeeze(); PL3_name = PL3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code3").send_keys(PL3_id); driver.find_element(By.NAME, "surname3").send_keys(PL3_name); driver.find_element(By.NAME, "position3").send_keys(positions[1])
        
        PL4 = deff.query('Name == "'+ players[3] +'"'); # query deff on tkinter input for player 4
        PL4_id = PL4.iloc[:,1:2].squeeze(); PL4_name = PL4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code4").send_keys(PL4_id); driver.find_element(By.NAME, "surname4").send_keys(PL4_name); driver.find_element(By.NAME, "position4").send_keys(positions[2])
        
        PL5 = deff.query('Name == "'+ players[4] +'"');         # query deff on tkinter input for player 5
        PL5_id = PL5.iloc[:,1:2].squeeze(); PL5_name = PL5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code5").send_keys(PL5_id); driver.find_element(By.NAME, "surname5").send_keys(PL5_name); driver.find_element(By.NAME, "position5").send_keys(positions[3])
        
        #--------------------------- Midfielders --------------------------#
        if formation == 532 or formation == 541:
            PL6 = deff.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver
        elif formation == 442 or formation == 451:
            PL6 = mid.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver            
        else:
            pass
            
        PL7 = mid.query('Name == "'+ players[6] +'"'); # query deff on tkinter input for player 7
        PL7_id = PL7.iloc[:,1:2].squeeze(); PL7_name = PL7.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code7").send_keys(PL7_id); driver.find_element(By.NAME, "surname7").send_keys(PL7_name); driver.find_element(By.NAME, "position7").send_keys(positions[5])
    
        PL8 = mid.query('Name == "'+ players[7] +'"'); # query deff on tkinter input for player 8
        PL8_id = PL8.iloc[:,1:2].squeeze(); PL8_name = PL8.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code8").send_keys(PL8_id); driver.find_element(By.NAME, "surname8").send_keys(PL8_name); driver.find_element(By.NAME, "position8").send_keys(positions[6])
        
        PL9 = mid.query('Name == "'+ players[8] +'"');         # query deff on tkinter input for player 9
        PL9_id = PL9.iloc[:,1:2].squeeze(); PL9_name = PL9.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code9").send_keys(PL9_id); driver.find_element(By.NAME, "surname9").send_keys(PL9_name); driver.find_element(By.NAME, "position9").send_keys(positions[7])
        
        #------------------------ Attackers ----------------------#
        if formation == 451 or formation == 541:
            PL10 = mid.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        elif formation == 442 or formation == 532:
            PL10 = att.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        else:
            pass
        
        PL11 = att.query('Name == "'+ players[10] +'"');         # query deff on tkinter input for player 11
        PL11_Pos = "RF"; PL11_id = PL11.iloc[:,1:2].squeeze(); PL11_name = PL11.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code11").send_keys(PL11_id); driver.find_element(By.NAME, "surname11").send_keys(PL11_name); driver.find_element(By.NAME, "position11").send_keys(positions[9])
    
        #------------------------ Substitutes ----------------------#
                        
        SUB1 = roles_df.query('Name == "'+ players[11] +'"'); # query deff on tkinter input for player 12
        SUB1_id = SUB1.iloc[:,0:1].squeeze(); SUB1_name = SUB1.iloc[:,1:2].squeeze();
        driver.find_element(By.NAME, "code12").send_keys(SUB1_id); driver.find_element(By.NAME, "surname12").send_keys(SUB1_name);
        
        SUB2 = DFA.query('Name == "'+ players[12] +'"'); # query deff on tkinter input for player 12
        SUB2_id = SUB2.iloc[:,1:2].squeeze(); SUB2_name = SUB2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code13").send_keys(SUB2_id); driver.find_element(By.NAME, "surname13").send_keys(SUB2_name);
    
        SUB3 = DFA.query('Name == "'+ players[13] +'"'); # query deff on tkinter input for player 12
        SUB3_id = SUB3.iloc[:,1:2].squeeze(); SUB3_name = SUB3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code14").send_keys(SUB3_id); driver.find_element(By.NAME, "surname14").send_keys(SUB3_name);
    
        SUB4 = DFA.query('Name == "'+ players[14] +'"'); # query deff on tkinter input for player 12
        SUB4_id = SUB4.iloc[:,1:2].squeeze(); SUB4_name = SUB4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code15").send_keys(SUB4_id); driver.find_element(By.NAME, "surname15").send_keys(SUB4_name);
    
        SUB5 = DFA.query('Name == "'+ players[15] +'"'); # query deff on tkinter input for player 12
        SUB5_id = SUB5.iloc[:,1:2].squeeze(); SUB5_name = SUB5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code16").send_keys(SUB5_id); driver.find_element(By.NAME, "surname16").send_keys(SUB5_name);


        #------------------------ Substitutes Options ----------------------#
        mins = subs.Minute.tolist()
        circ = subs.Circumstance.tolist()
        play_on = subs["Player On"].tolist()
        play_off = subs["Player Off"].tolist()
        new_pos = subs.Position.tolist()
        
        driver.find_element(By.NAME, "min").send_keys(mins[0]);
        driver.find_element(By.NAME, "Circ").send_keys(circ[0]);
        PLON1 = roles_df.query('Name == "'+ play_on[0] +'"'); PLON1_id = PLON1.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn").send_keys(PLON1_id);
        PLOFF1 = roles_df.query('Name == "'+ play_off[0] +'"'); PLOFF1_id = PLOFF1.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff").send_keys(PLOFF1_id);
        driver.find_element(By.NAME, "Newposition").send_keys(new_pos[0]);

        driver.find_element(By.NAME, "min2").send_keys(mins[1]);
        driver.find_element(By.NAME, "Circ2").send_keys(circ[1]);
        PLON2 = roles_df.query('Name == "'+ play_on[1] +'"'); PLON2_id = PLON2.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn2").send_keys(PLON2_id);
        PLOFF2 = roles_df.query('Name == "'+ play_off[1] +'"'); PLOFF2_id = PLOFF2.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff2").send_keys(PLOFF2_id);
        driver.find_element(By.NAME, "Newposition2").send_keys(new_pos[1]);
        
        driver.find_element(By.NAME, "min3").send_keys(mins[2]);
        driver.find_element(By.NAME, "Circ3").send_keys(circ[2]);
        PLON3 = roles_df.query('Name == "'+ play_on[2] +'"'); PLON3_id = PLON3.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn3").send_keys(PLON3_id);
        PLOFF3 = roles_df.query('Name == "'+ play_off[2] +'"'); PLOFF3_id = PLOFF3.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff3").send_keys(PLOFF3_id);
        driver.find_element(By.NAME, "Newposition3").send_keys(new_pos[2]);

        driver.find_element(By.NAME, "min4").send_keys(mins[3]);
        driver.find_element(By.NAME, "Circ4").send_keys(circ[3]);
        PLON4 = roles_df.query('Name == "'+ play_on[3] +'"'); PLON4_id = PLON4.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn4").send_keys(PLON4_id);
        PLOFF4 = roles_df.query('Name == "'+ play_off[3] +'"'); PLOFF4_id = PLOFF4.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff4").send_keys(PLOFF4_id);
        driver.find_element(By.NAME, "Newposition4").send_keys(new_pos[3]);

        driver.find_element(By.NAME, "min5").send_keys(mins[4]);
        driver.find_element(By.NAME, "Circ5").send_keys(circ[4]);
        PLON5 = roles_df.query('Name == "'+ play_on[4] +'"'); PLON5_id = PLON5.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn5").send_keys(PLON5_id);
        PLOFF5 = roles_df.query('Name == "'+ play_off[4] +'"'); PLOFF5_id = PLOFF5.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff5").send_keys(PLOFF5_id);
        driver.find_element(By.NAME, "Newposition5").send_keys(new_pos[4]);
        
        # Capt / FK / Pen
        CAP = roles_df.query('Name == "'+ roles[0] +'"');
        CAP_id = CAP.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Capt").send_keys(CAP_id)
        FRK = roles_df.query('Name == "'+ roles[1] +'"');
        FRK_id = FRK.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Freekick").send_keys(FRK_id)
        PEN = roles_df.query('Name == "'+ roles[2] +'"');
        PEN_id = PEN.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Penalty").send_keys(PEN_id)
        
        # ============================ tactics ============================ #
        print(tactics)
        # Function to send keys with a delay


        # Fill in the form
        driver.find_element(By.NAME, "tactic").send_keys(tactics[0])
        driver.find_element(By.NAME, "tactic2").send_keys(tactics[1])
    
        if tactics[2] == "PP":
            dropdown = Select(driver.find_element(By.NAME, "tactic3"))
            dropdown.select_by_index(5)
        else:
            driver.find_element(By.NAME, "tactic3").send_keys(tactics[2])

        if tactics[3] == "PP":
            dropdown = Select(driver.find_element(By.NAME, "tactic4"))
            dropdown.select_by_index(5)
        else:
            driver.find_element(By.NAME, "tactic4").send_keys(tactics[3])
            
        driver.find_element(By.NAME, "tactic5").send_keys(tactics[4])
        driver.find_element(By.NAME, "tactic6").send_keys(tactics[5])
        
        if tactics[6] == "PP":
            dropdown = Select(driver.find_element(By.NAME, "textfield3"))
            dropdown.select_by_index(13)
        else:
            driver.find_element(By.NAME, "textfield3").send_keys(tactics[6])
        
        # training
        driver.find_element(By.NAME, "train").send_keys(training[0])
        driver.find_element(By.NAME, "train2").send_keys(training[1])
        driver.find_element(By.NAME, "train3").send_keys(training[2])
        driver.find_element(By.NAME, "train4").send_keys(training[3])
        driver.find_element(By.NAME, "train5").send_keys(training[4])
        driver.find_element(By.NAME, "train6").send_keys(training[5])
        driver.find_element(By.NAME, "train7").send_keys(training[6])
        driver.find_element(By.NAME, "train8").send_keys(training[7])
        driver.find_element(By.NAME, "train9").send_keys(training[8])
        driver.find_element(By.NAME, "train10").send_keys(training[9])

        # ======================= ACTIONS ========================= #
        act1 = roles_df.query('Name == "'+ names[0] +'"'); action_id1 = act1.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id").send_keys(action_id1); 
        driver.find_element(By.NAME, "action_name").send_keys(names[0]); 
        driver.find_element(By.NAME, "action").send_keys(actions[0])
        driver.find_element(By.NAME, "actionsub").send_keys(SPS[0])
        
        act2 = roles_df.query('Name == "'+ names[1] +'"'); action_id2 = act2.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id2").send_keys(action_id2); 
        driver.find_element(By.NAME, "action_name2").send_keys(names[1]); 
        driver.find_element(By.NAME, "action2").send_keys(actions[1])
        driver.find_element(By.NAME, "actionsub2").send_keys(SPS[1])

        act3 = roles_df.query('Name == "'+ names[2] +'"'); action_id3 = act3.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id3").send_keys(action_id3); 
        driver.find_element(By.NAME, "action_name3").send_keys(names[2]); 
        driver.find_element(By.NAME, "action3").send_keys(actions[2])

        act4 = roles_df.query('Name == "'+ names[3] +'"'); action_id4 = act4.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id4").send_keys(action_id4); 
        driver.find_element(By.NAME, "action_name4").send_keys(names[3]); 
        driver.find_element(By.NAME, "action4").send_keys(actions[3])

        act5 = roles_df.query('Name == "'+ names[4] +'"'); action_id5 = act5.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id5").send_keys(action_id5); 
        driver.find_element(By.NAME, "action_name5").send_keys(names[4]); 
        driver.find_element(By.NAME, "action5").send_keys(actions[4])

        act6 = roles_df.query('Name == "'+ names[5] +'"'); action_id6 = act6.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id6").send_keys(action_id6); 
        driver.find_element(By.NAME, "action_name6").send_keys(names[5]); 
        driver.find_element(By.NAME, "action6").send_keys(actions[5])

        act7 = roles_df.query('Name == "'+ names[6] +'"'); action_id7 = act7.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id7").send_keys(action_id7); 
        driver.find_element(By.NAME, "action_name7").send_keys(names[6]); 
        driver.find_element(By.NAME, "action7").send_keys(actions[6])

        act8 = roles_df.query('Name == "'+ names[7] +'"'); action_id8 = act8.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id8").send_keys(action_id8); 
        driver.find_element(By.NAME, "action_name8").send_keys(names[7]); 
        driver.find_element(By.NAME, "action8").send_keys(actions[7])

        act9 = roles_df.query('Name == "'+ names[8] +'"'); action_id9 = act9.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id9").send_keys(action_id9); 
        driver.find_element(By.NAME, "action_name9").send_keys(names[8]); 
        driver.find_element(By.NAME, "action9").send_keys(actions[8])

        act10 = roles_df.query('Name == "'+ names[9] +'"'); action_id10 = act10.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id10").send_keys(action_id10); 
        driver.find_element(By.NAME, "action_name10").send_keys(names[9]); 
        driver.find_element(By.NAME, "action10").send_keys(actions[9])

        ax = pd.DataFrame({"Player" :names, "Action" : actions})
        choochoo = pd.DataFrame({"Training":training})
        
        #------------------------- write players to excel sheet --------------------#
        df = pd.DataFrame(positions,players[1:])
        df.reset_index(inplace=True)
        df.columns = ["Player","Pos" ]    

        tix = pd.DataFrame(tactics)
        tix.columns=["Tactics"]

        roles = pd.DataFrame(roles)
        roles.columns=["Role"]

        formations = {"Formation": [formation]}
        fo = pd.DataFrame(formations)
        
        
        with pd.ExcelWriter("Weekly Submissions/Weekly Sub.xlsx") as writer:
            df.to_excel(writer, sheet_name="ft",index=True)
            tix.to_excel(writer, sheet_name="tactics",index=True)
            roles.to_excel(writer, sheet_name="roles",index=True)
            choochoo.to_excel(writer, sheet_name="training",index=True)
            ax.to_excel(writer, sheet_name="actions",index=True)
            fo.to_excel(writer, sheet_name="formations",index=True)
            subs.to_excel(writer, sheet_name="subs",index=True)
            
        get_scouts = pd.read_csv("Scouts/Scouted this week.csv")
        scouts = get_scouts["TEA Random"].tolist()

        
        # append scouts
        # List of element names corresponding to each scout
        element_names = [
            "extra", "extra2", "extra3", "extra4", "extra5",
            "extra6", "extra7", "extra8", "extra9", "extra10"
        ]
        
        # Loop through the scouts list and element names
        for i in range(min(len(scouts), len(element_names))):
            driver.find_element(By.NAME, element_names[i]).send_keys(scouts[i])

        # select same tactics
        if ticks[0] == 1:
            driver.find_element(By.NAME, "tactic722").click()
        else:
            pass
        if ticks[1] == 1:
            driver.find_element(By.NAME, "tactic723").click()
        else:
            pass
            
        driver.find_element(By.NAME, "textfield").send_keys(message) # enter message
        
        driver.find_element(By.NAME, "password").send_keys("password123") # enter password

# ======================================================================================================================= #    
# ================================================== SUBMIT RESERVE TEAM ================================================== #
# ======================================================================================================================= #    
    def submit_res_team(self, players, positions, tactics, roles, roles_df, actions, names, password, formation, subs):
        driver = webdriver.Firefox() # open firefox
        driver.maximize_window() # full screen
        driver.get("http://www.ultimate-europe.co.uk/mds_form4.htm") # get the web address

#=========== Get/Enter MDS details ===========#
        turn_data = pd.read_csv("Turn Data/Turn Data.csv")
        duedate = turn_data.Deadline.squeeze()
        team_id = turn_data.TeamID.squeeze()
        team = turn_data.Team.squeeze()
        mgr = turn_data.Manager.squeeze()
        email = turn_data.Email.squeeze()
        game = turn_data.Game.squeeze()
        turn = turn_data.Turn.squeeze()
        season = turn_data.Season.squeeze()
        
        # append mds details
        driver.find_element(By.NAME, "email").send_keys(email) #email
        driver.find_element(By.NAME, "deadline").send_keys(duedate) #deadline
        driver.find_element(By.NAME, "id").send_keys(team_id) #teamid
        driver.find_element(By.NAME, "team").send_keys(team) #teamname
        driver.find_element(By.NAME, "manager").send_keys(mgr) #manager name
        driver.find_element(By.NAME, "game").send_keys(int(game)) #game number
        driver.find_element(By.NAME, "season").send_keys(int(season)) #season number
        driver.find_element(By.NAME, "turn").send_keys(int(turn)) # turn number

        file = "Turn Data/Show Team.xlsx"
        gks = pd.read_excel(open(file,"rb"), sheet_name="r_gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="r_deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="r_mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="r_att")
        DFA = pd.concat([deff,mid,att])

        #--------------------------- Goalkeepers --------------------------#
        PL1 = gks.query('Name == "'+ players[0] +'"'); 
        PL1_id = PL1.iloc[:,1:2].squeeze(); PL1_name = PL1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code").send_keys(PL1_id); driver.find_element(By.NAME, "surname").send_keys(PL1_name);
        
        #--------------------------- Defenders --------------------------#
        PL2 = deff.query('Name == "'+ players[1] +'"'); 
        PL2_id = PL2.iloc[:,1:2].squeeze(); PL2_name = PL2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code2").send_keys(PL2_id); driver.find_element(By.NAME, "surname2").send_keys(PL2_name); driver.find_element(By.NAME, "position2").send_keys(positions[0])

        PL3 = deff.query('Name == "'+ players[2] +'"');          # query deff on tkinter input for player 3
        PL3_Pos = "CB"; PL3_id = PL3.iloc[:,1:2].squeeze(); PL3_name = PL3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code3").send_keys(PL3_id); driver.find_element(By.NAME, "surname3").send_keys(PL3_name); driver.find_element(By.NAME, "position3").send_keys(positions[1])
        
        PL4 = deff.query('Name == "'+ players[3] +'"'); # query deff on tkinter input for player 4
        PL4_id = PL4.iloc[:,1:2].squeeze(); PL4_name = PL4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code4").send_keys(PL4_id); driver.find_element(By.NAME, "surname4").send_keys(PL4_name); driver.find_element(By.NAME, "position4").send_keys(positions[2])
        
        PL5 = deff.query('Name == "'+ players[4] +'"');         # query deff on tkinter input for player 5
        PL5_id = PL5.iloc[:,1:2].squeeze(); PL5_name = PL5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code5").send_keys(PL5_id); driver.find_element(By.NAME, "surname5").send_keys(PL5_name); driver.find_element(By.NAME, "position5").send_keys(positions[3])
        
        #--------------------------- Midfielders --------------------------#
        if formation == 532 or formation == 541:
            PL6 = deff.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver
        elif formation == 442 or formation == 451:
            PL6 = mid.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver            
        else:
            pass
            
        PL7 = mid.query('Name == "'+ players[6] +'"'); # query deff on tkinter input for player 7
        PL7_id = PL7.iloc[:,1:2].squeeze(); PL7_name = PL7.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code7").send_keys(PL7_id); driver.find_element(By.NAME, "surname7").send_keys(PL7_name); driver.find_element(By.NAME, "position7").send_keys(positions[5])
    
        PL8 = mid.query('Name == "'+ players[7] +'"'); # query deff on tkinter input for player 8
        PL8_id = PL8.iloc[:,1:2].squeeze(); PL8_name = PL8.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code8").send_keys(PL8_id); driver.find_element(By.NAME, "surname8").send_keys(PL8_name); driver.find_element(By.NAME, "position8").send_keys(positions[6])
        
        PL9 = mid.query('Name == "'+ players[8] +'"');         # query deff on tkinter input for player 9
        PL9_id = PL9.iloc[:,1:2].squeeze(); PL9_name = PL9.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code9").send_keys(PL9_id); driver.find_element(By.NAME, "surname9").send_keys(PL9_name); driver.find_element(By.NAME, "position9").send_keys(positions[7])
        
        #------------------------ Attackers ----------------------#
        if formation == 451 or formation == 541:
            PL10 = mid.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        elif formation == 442 or formation == 532:
            PL10 = att.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        else:
            pass
        
        PL11 = att.query('Name == "'+ players[10] +'"');         # query deff on tkinter input for player 11
        PL11_Pos = "RF"; PL11_id = PL11.iloc[:,1:2].squeeze(); PL11_name = PL11.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code11").send_keys(PL11_id); driver.find_element(By.NAME, "surname11").send_keys(PL11_name); driver.find_element(By.NAME, "position11").send_keys(positions[9])
    
        #------------------------ Substitutes ----------------------#
                        
        SUB1 = gks.query('Name == "'+ players[11] +'"'); # query deff on tkinter input for player 12
        SUB1_id = SUB1.iloc[:,1:2].squeeze(); SUB1_name = SUB1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code12").send_keys(SUB1_id); driver.find_element(By.NAME, "surname12").send_keys(SUB1_name);
        
        SUB2 = DFA.query('Name == "'+ players[12] +'"'); # query deff on tkinter input for player 12
        SUB2_id = SUB2.iloc[:,1:2].squeeze(); SUB2_name = SUB2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code13").send_keys(SUB2_id); driver.find_element(By.NAME, "surname13").send_keys(SUB2_name);
    
        SUB3 = DFA.query('Name == "'+ players[13] +'"'); # query deff on tkinter input for player 12
        SUB3_id = SUB3.iloc[:,1:2].squeeze(); SUB3_name = SUB3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code14").send_keys(SUB3_id); driver.find_element(By.NAME, "surname14").send_keys(SUB3_name);
    
        SUB4 = DFA.query('Name == "'+ players[14] +'"'); # query deff on tkinter input for player 12
        SUB4_id = SUB4.iloc[:,1:2].squeeze(); SUB4_name = SUB4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code15").send_keys(SUB4_id); driver.find_element(By.NAME, "surname15").send_keys(SUB4_name);
    
        SUB5 = DFA.query('Name == "'+ players[15] +'"'); # query deff on tkinter input for player 12
        SUB5_id = SUB5.iloc[:,1:2].squeeze(); SUB5_name = SUB5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code16").send_keys(SUB5_id); driver.find_element(By.NAME, "surname16").send_keys(SUB5_name);

        #------------------------ Substitutes Options ----------------------#
        mins = subs.Minute.tolist()
        circ = subs.Circumstance.tolist()
        play_on = subs["Player On"].tolist()
        play_off = subs["Player Off"].tolist()
        new_pos = subs.Position.tolist()
        
        driver.find_element(By.NAME, "min").send_keys(mins[0]);
        driver.find_element(By.NAME, "Circ").send_keys(circ[0]);
        PLON1 = roles_df.query('Name == "'+ play_on[0] +'"'); PLON1_id = PLON1.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn").send_keys(PLON1_id);
        PLOFF1 = roles_df.query('Name == "'+ play_off[0] +'"'); PLOFF1_id = PLOFF1.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff").send_keys(PLOFF1_id);
        driver.find_element(By.NAME, "NewPosition").send_keys(new_pos[0]);

        driver.find_element(By.NAME, "min2").send_keys(mins[1]);
        driver.find_element(By.NAME, "Circ2").send_keys(circ[1]);
        PLON2 = roles_df.query('Name == "'+ play_on[1] +'"'); PLON2_id = PLON2.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn2").send_keys(PLON2_id);
        PLOFF2 = roles_df.query('Name == "'+ play_off[1] +'"'); PLOFF2_id = PLOFF2.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff2").send_keys(PLOFF2_id);
        driver.find_element(By.NAME, "NewPosition2").send_keys(new_pos[1]);
        
        driver.find_element(By.NAME, "min3").send_keys(mins[2]);
        driver.find_element(By.NAME, "Circ3").send_keys(circ[2]);
        PLON3 = roles_df.query('Name == "'+ play_on[2] +'"'); PLON3_id = PLON3.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn3").send_keys(PLON3_id);
        PLOFF3 = roles_df.query('Name == "'+ play_off[2] +'"'); PLOFF3_id = PLOFF3.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff3").send_keys(PLOFF3_id);
        driver.find_element(By.NAME, "NewPosition3").send_keys(new_pos[2]);

        driver.find_element(By.NAME, "min4").send_keys(mins[3]);
        driver.find_element(By.NAME, "Circ4").send_keys(circ[3]);
        PLON4 = roles_df.query('Name == "'+ play_on[3] +'"'); PLON4_id = PLON4.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn4").send_keys(PLON4_id);
        PLOFF4 = roles_df.query('Name == "'+ play_off[3] +'"'); PLOFF4_id = PLOFF4.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff4").send_keys(PLOFF4_id);
        driver.find_element(By.NAME, "NewPosition4").send_keys(new_pos[3]);

        driver.find_element(By.NAME, "min5").send_keys(mins[4]);
        driver.find_element(By.NAME, "Circ5").send_keys(circ[4]);
        PLON5 = roles_df.query('Name == "'+ play_on[4] +'"'); PLON5_id = PLON5.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn5").send_keys(PLON5_id);
        PLOFF5 = roles_df.query('Name == "'+ play_off[4] +'"'); PLOFF5_id = PLOFF5.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff5").send_keys(PLOFF5_id);
        driver.find_element(By.NAME, "NewPosition5").send_keys(new_pos[4]);
        
        # Fill in the form
        driver.find_element(By.NAME, "tactic").send_keys(tactics[0])
        driver.find_element(By.NAME, "tactic2").send_keys(tactics[1])
    
        if tactics[2] == "PP":
            dropdown = Select(driver.find_element(By.NAME, "tactic3"))
            dropdown.select_by_index(5)
        else:
            driver.find_element(By.NAME, "tactic3").send_keys(tactics[2])

        if tactics[3] == "PP":
            dropdown = Select(driver.find_element(By.NAME, "tactic4"))
            dropdown.select_by_index(5)
        else:
            driver.find_element(By.NAME, "tactic4").send_keys(tactics[3])
            
        driver.find_element(By.NAME, "tactic5").send_keys(tactics[4])
        driver.find_element(By.NAME, "tactic6").send_keys(tactics[5])
        
        if tactics[6] == "PP":
            dropdown = Select(driver.find_element(By.NAME, "textfield3"))
            dropdown.select_by_index(13)
        else:
            driver.find_element(By.NAME, "textfield3").send_keys(tactics[6])
        
        
        # Capt / FK / Pen
        CAP = roles_df.query('Name == "'+ roles[0] +'"');
        CAP_id = CAP.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Capt").send_keys(CAP_id)
        FRK = roles_df.query('Name == "'+ roles[1] +'"');
        FRK_id = FRK.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Freekick").send_keys(FRK_id)
        PEN = roles_df.query('Name == "'+ roles[2] +'"');
        PEN_id = PEN.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Penalty").send_keys(PEN_id)

        # ======================= ACTIONS ========================= #
        act1 = roles_df.query('Name == "'+ names[0] +'"'); action_id1 = act1.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id").send_keys(action_id1); 
        driver.find_element(By.NAME, "action_name").send_keys(names[0]); 
        driver.find_element(By.NAME, "action").send_keys(actions[0])
        
        act2 = roles_df.query('Name == "'+ names[1] +'"'); action_id2 = act2.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id2").send_keys(action_id2); 
        driver.find_element(By.NAME, "action_name2").send_keys(names[1]); 
        driver.find_element(By.NAME, "action2").send_keys(actions[1])

        act3 = roles_df.query('Name == "'+ names[2] +'"'); action_id3 = act3.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id3").send_keys(action_id3); 
        driver.find_element(By.NAME, "action_name3").send_keys(names[2]); 
        driver.find_element(By.NAME, "action3").send_keys(actions[2])

        act4 = roles_df.query('Name == "'+ names[3] +'"'); action_id4 = act4.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id4").send_keys(action_id4); 
        driver.find_element(By.NAME, "action_name4").send_keys(names[3]); 
        driver.find_element(By.NAME, "action4").send_keys(actions[3])

        act5 = roles_df.query('Name == "'+ names[4] +'"'); action_id5 = act5.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id5").send_keys(action_id5); 
        driver.find_element(By.NAME, "action_name5").send_keys(names[4]); 
        driver.find_element(By.NAME, "action5").send_keys(actions[4])

        driver.find_element(By.NAME, "password").send_keys(password) # enter password
        

        
        #------------------------- write players to excel sheet --------------------#
        df = pd.DataFrame(positions,players[1:])
        df.reset_index(inplace=True)
        df.columns = ["Player","Pos" ]    
        
        ax = pd.DataFrame({"Player" :names, "Action" : actions})
        
        tix = pd.DataFrame(tactics)
        tix.columns=["Tactics"]

        roles = pd.DataFrame(roles)
        roles.columns=["Role"]

        formations = {"Formation": [formation]}
        fo = pd.DataFrame(formations)
        
        with pd.ExcelWriter("Weekly Submissions/Weekly Res Sub.xlsx") as writer:
            df.to_excel(writer, sheet_name="ft",index=True)
            tix.to_excel(writer, sheet_name="tactics",index=True)
            roles.to_excel(writer, sheet_name="roles",index=True)
            ax.to_excel(writer, sheet_name="actions",index=True)
            fo.to_excel(writer, sheet_name="formations",index=True)
            subs.to_excel(writer, sheet_name="subs",index=True)

# ======================================================================================================================= #    
# ================================================== SUBMIT YOUTH TEAM ================================================== #
# ======================================================================================================================= #    
    def submit_yth_team(self, players, positions, tactics, roles, roles_df, actions, names, password, formation,subs):
        print(f'Rxd formation is {formation}')
        driver = webdriver.Firefox() # open firefox
        driver.maximize_window() # full screen
        driver.get("http://www.ultimate-europe.co.uk/mds_form5.htm") # get the web address

#=========== Get/Enter MDS details ===========#
        turn_data = pd.read_csv("Turn Data/Turn Data.csv")
        duedate = turn_data.Deadline.squeeze()
        team_id = turn_data.TeamID.squeeze()
        team = turn_data.Team.squeeze()
        mgr = turn_data.Manager.squeeze()
        email = turn_data.Email.squeeze()
        game = turn_data.Game.squeeze()
        turn = turn_data.Turn.squeeze()
        season = turn_data.Season.squeeze()
        
        # append mds details
        driver.find_element(By.NAME, "email").send_keys(email) #email
        driver.find_element(By.NAME, "deadline").send_keys(duedate) #deadline
        driver.find_element(By.NAME, "id").send_keys(team_id) #teamid
        driver.find_element(By.NAME, "team").send_keys(team) #teamname
        driver.find_element(By.NAME, "manager").send_keys(mgr) #manager name
        driver.find_element(By.NAME, "game").send_keys(int(game)) #game number
        driver.find_element(By.NAME, "season").send_keys(int(season)) #season number
        driver.find_element(By.NAME, "turn").send_keys(int(turn)) # turn number

        file = "Turn Data/Show Team.xlsx"
        gks = pd.read_excel(open(file,"rb"), sheet_name="y_gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="y_deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="y_mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="y_att")
        DFA = pd.concat([deff,mid,att])

        #--------------------------- Goalkeepers --------------------------#
        PL1 = gks.query('Name == "'+ players[0] +'"'); 
        PL1_id = PL1.iloc[:,1:2].squeeze(); PL1_name = PL1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code").send_keys(PL1_id); driver.find_element(By.NAME, "surname").send_keys(PL1_name);
        
        #--------------------------- Defenders --------------------------#
        PL2 = deff.query('Name == "'+ players[1] +'"'); 
        PL2_id = PL2.iloc[:,1:2].squeeze(); PL2_name = PL2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code2").send_keys(PL2_id); driver.find_element(By.NAME, "surname2").send_keys(PL2_name); driver.find_element(By.NAME, "position2").send_keys(positions[0])

        PL3 = deff.query('Name == "'+ players[2] +'"');          # query deff on tkinter input for player 3
        PL3_Pos = "CB"; PL3_id = PL3.iloc[:,1:2].squeeze(); PL3_name = PL3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code3").send_keys(PL3_id); driver.find_element(By.NAME, "surname3").send_keys(PL3_name); driver.find_element(By.NAME, "position3").send_keys(positions[1])
        
        PL4 = deff.query('Name == "'+ players[3] +'"'); # query deff on tkinter input for player 4
        PL4_id = PL4.iloc[:,1:2].squeeze(); PL4_name = PL4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code4").send_keys(PL4_id); driver.find_element(By.NAME, "surname4").send_keys(PL4_name); driver.find_element(By.NAME, "position4").send_keys(positions[2])
        
        PL5 = deff.query('Name == "'+ players[4] +'"');         # query deff on tkinter input for player 5
        PL5_id = PL5.iloc[:,1:2].squeeze(); PL5_name = PL5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code5").send_keys(PL5_id); driver.find_element(By.NAME, "surname5").send_keys(PL5_name); driver.find_element(By.NAME, "position5").send_keys(positions[3])
        
        #--------------------------- Midfielders --------------------------#
        if formation == 532 or formation == 541:
            PL6 = deff.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver
        elif formation == 442 or formation == 451:
            PL6 = mid.query('Name == "'+ players[5] +'"');     # query deff on tkinter input for player 6
            PL6_id = PL6.iloc[:,1:2].squeeze(); PL6_name = PL6.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code6").send_keys(PL6_id); driver.find_element(By.NAME, "surname6").send_keys(PL6_name); driver.find_element(By.NAME, "position6").send_keys(positions[4])    # send elements to web driver            
        else:
            pass
            
        PL7 = mid.query('Name == "'+ players[6] +'"'); # query deff on tkinter input for player 7
        PL7_id = PL7.iloc[:,1:2].squeeze(); PL7_name = PL7.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code7").send_keys(PL7_id); driver.find_element(By.NAME, "surname7").send_keys(PL7_name); driver.find_element(By.NAME, "position7").send_keys(positions[5])
    
        PL8 = mid.query('Name == "'+ players[7] +'"'); # query deff on tkinter input for player 8
        PL8_id = PL8.iloc[:,1:2].squeeze(); PL8_name = PL8.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code8").send_keys(PL8_id); driver.find_element(By.NAME, "surname8").send_keys(PL8_name); driver.find_element(By.NAME, "position8").send_keys(positions[6])
        
        PL9 = mid.query('Name == "'+ players[8] +'"');         # query deff on tkinter input for player 9
        PL9_id = PL9.iloc[:,1:2].squeeze(); PL9_name = PL9.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code9").send_keys(PL9_id); driver.find_element(By.NAME, "surname9").send_keys(PL9_name); driver.find_element(By.NAME, "position9").send_keys(positions[7])
        
        #------------------------ Attackers ----------------------#
        if formation == 451 or formation == 541:
            PL10 = mid.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        elif formation == 442 or formation == 532:
            PL10 = att.query('Name == "'+ players[9] +'"');         # query deff on tkinter input for player 10
            PL10_id = PL10.iloc[:,1:2].squeeze(); PL10_name = PL10.iloc[:,2:3].squeeze();
            driver.find_element(By.NAME, "code10").send_keys(PL10_id); driver.find_element(By.NAME, "surname10").send_keys(PL10_name); driver.find_element(By.NAME, "position10").send_keys(positions[8])
        else:
            pass
            
        PL11 = att.query('Name == "'+ players[10] +'"');         # query deff on tkinter input for player 11
        PL11_Pos = "RF"; PL11_id = PL11.iloc[:,1:2].squeeze(); PL11_name = PL11.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code11").send_keys(PL11_id); driver.find_element(By.NAME, "surname11").send_keys(PL11_name); driver.find_element(By.NAME, "position11").send_keys(positions[9])
    
        #------------------------ Substitutes ----------------------#
                        
        SUB1 = gks.query('Name == "'+ players[11] +'"'); # query deff on tkinter input for player 12
        SUB1_id = SUB1.iloc[:,1:2].squeeze(); SUB1_name = SUB1.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code12").send_keys(SUB1_id); driver.find_element(By.NAME, "surname12").send_keys(SUB1_name);
        
        SUB2 = DFA.query('Name == "'+ players[12] +'"'); # query deff on tkinter input for player 12
        SUB2_id = SUB2.iloc[:,1:2].squeeze(); SUB2_name = SUB2.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code13").send_keys(SUB2_id); driver.find_element(By.NAME, "surname13").send_keys(SUB2_name);
    
        SUB3 = DFA.query('Name == "'+ players[13] +'"'); # query deff on tkinter input for player 12
        SUB3_id = SUB3.iloc[:,1:2].squeeze(); SUB3_name = SUB3.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code14").send_keys(SUB3_id); driver.find_element(By.NAME, "surname14").send_keys(SUB3_name);
    
        SUB4 = DFA.query('Name == "'+ players[14] +'"'); # query deff on tkinter input for player 12
        SUB4_id = SUB4.iloc[:,1:2].squeeze(); SUB4_name = SUB4.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code15").send_keys(SUB4_id); driver.find_element(By.NAME, "surname15").send_keys(SUB4_name);
    
        SUB5 = DFA.query('Name == "'+ players[15] +'"'); # query deff on tkinter input for player 12
        SUB5_id = SUB5.iloc[:,1:2].squeeze(); SUB5_name = SUB5.iloc[:,2:3].squeeze();
        driver.find_element(By.NAME, "code16").send_keys(SUB5_id); driver.find_element(By.NAME, "surname16").send_keys(SUB5_name);

        #------------------------ Substitutes Options ----------------------#
        mins = subs.Minute.tolist()
        circ = subs.Circumstance.tolist()
        play_on = subs["Player On"].tolist()
        play_off = subs["Player Off"].tolist()
        new_pos = subs.Position.tolist()
        
        driver.find_element(By.NAME, "min").send_keys(mins[0]);
        driver.find_element(By.NAME, "Circ").send_keys(circ[0]);
        PLON1 = roles_df.query('Name == "'+ play_on[0] +'"'); PLON1_id = PLON1.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn").send_keys(PLON1_id);
        PLOFF1 = roles_df.query('Name == "'+ play_off[0] +'"'); PLOFF1_id = PLOFF1.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff").send_keys(PLOFF1_id);
        driver.find_element(By.NAME, "NewPosition").send_keys(new_pos[0]);

        driver.find_element(By.NAME, "min2").send_keys(mins[1]);
        driver.find_element(By.NAME, "Circ2").send_keys(circ[1]);
        PLON2 = roles_df.query('Name == "'+ play_on[1] +'"'); PLON2_id = PLON2.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn2").send_keys(PLON2_id);
        PLOFF2 = roles_df.query('Name == "'+ play_off[1] +'"'); PLOFF2_id = PLOFF2.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff2").send_keys(PLOFF2_id);
        driver.find_element(By.NAME, "NewPosition2").send_keys(new_pos[1]);
        
        driver.find_element(By.NAME, "min3").send_keys(mins[2]);
        driver.find_element(By.NAME, "Circ3").send_keys(circ[2]);
        PLON3 = roles_df.query('Name == "'+ play_on[2] +'"'); PLON3_id = PLON3.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn3").send_keys(PLON3_id);
        PLOFF3 = roles_df.query('Name == "'+ play_off[2] +'"'); PLOFF3_id = PLOFF3.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff3").send_keys(PLOFF3_id);
        driver.find_element(By.NAME, "NewPosition3").send_keys(new_pos[2]);

        driver.find_element(By.NAME, "min4").send_keys(mins[3]);
        driver.find_element(By.NAME, "Circ4").send_keys(circ[3]);
        PLON4 = roles_df.query('Name == "'+ play_on[3] +'"'); PLON4_id = PLON4.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn4").send_keys(PLON4_id);
        PLOFF4 = roles_df.query('Name == "'+ play_off[3] +'"'); PLOFF4_id = PLOFF4.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff4").send_keys(PLOFF4_id);
        driver.find_element(By.NAME, "NewPosition4").send_keys(new_pos[3]);

        driver.find_element(By.NAME, "min5").send_keys(mins[4]);
        driver.find_element(By.NAME, "Circ5").send_keys(circ[4]);
        PLON5 = roles_df.query('Name == "'+ play_on[4] +'"'); PLON5_id = PLON5.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOn5").send_keys(PLON5_id);
        PLOFF5 = roles_df.query('Name == "'+ play_off[4] +'"'); PLOFF5_id = PLOFF5.iloc[:,0:1].squeeze(); driver.find_element(By.NAME, "PlayerOff5").send_keys(PLOFF5_id);
        driver.find_element(By.NAME, "NewPosition5").send_keys(new_pos[4]);
        
        # Fill in the form
        driver.find_element(By.NAME, "tactic").send_keys(tactics[0])
        driver.find_element(By.NAME, "tactic2").send_keys(tactics[1])
    
        if tactics[2] == "PP":
            dropdown = Select(driver.find_element(By.NAME, "tactic3"))
            dropdown.select_by_index(5)
        else:
            driver.find_element(By.NAME, "tactic3").send_keys(tactics[2])

        if tactics[3] == "PP":
            dropdown = Select(driver.find_element(By.NAME, "tactic4"))
            dropdown.select_by_index(5)
        else:
            driver.find_element(By.NAME, "tactic4").send_keys(tactics[3])
            
        driver.find_element(By.NAME, "tactic5").send_keys(tactics[4])
        driver.find_element(By.NAME, "tactic6").send_keys(tactics[5])
        
        if tactics[6] == "PP":
            dropdown = Select(driver.find_element(By.NAME, "textfield3"))
            dropdown.select_by_index(13)
        else:
            driver.find_element(By.NAME, "textfield3").send_keys(tactics[6])
        
        
        # Capt / FK / Pen
        CAP = roles_df.query('Name == "'+ roles[0] +'"');
        CAP_id = CAP.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Capt").send_keys(CAP_id)
        FRK = roles_df.query('Name == "'+ roles[1] +'"');
        FRK_id = FRK.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Freekick").send_keys(FRK_id)
        PEN = roles_df.query('Name == "'+ roles[2] +'"');
        PEN_id = PEN.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "Penalty").send_keys(PEN_id)

        # ======================= ACTIONS ========================= #
        act1 = roles_df.query('Name == "'+ names[0] +'"'); action_id1 = act1.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id").send_keys(action_id1); 
        driver.find_element(By.NAME, "action_name").send_keys(names[0]); 
        driver.find_element(By.NAME, "action").send_keys(actions[0])
        
        act2 = roles_df.query('Name == "'+ names[1] +'"'); action_id2 = act2.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id2").send_keys(action_id2); 
        driver.find_element(By.NAME, "action_name2").send_keys(names[1]); 
        driver.find_element(By.NAME, "action2").send_keys(actions[1])

        act3 = roles_df.query('Name == "'+ names[2] +'"'); action_id3 = act3.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id3").send_keys(action_id3); 
        driver.find_element(By.NAME, "action_name3").send_keys(names[2]); 
        driver.find_element(By.NAME, "action3").send_keys(actions[2])

        act4 = roles_df.query('Name == "'+ names[3] +'"'); action_id4 = act4.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id4").send_keys(action_id4); 
        driver.find_element(By.NAME, "action_name4").send_keys(names[3]); 
        driver.find_element(By.NAME, "action4").send_keys(actions[3])

        act5 = roles_df.query('Name == "'+ names[4] +'"'); action_id5 = act5.iloc[:,0:1].squeeze();
        driver.find_element(By.NAME, "action_id5").send_keys(action_id5); 
        driver.find_element(By.NAME, "action_name5").send_keys(names[4]); 
        driver.find_element(By.NAME, "action5").send_keys(actions[4])

        driver.find_element(By.NAME, "password").send_keys(password) # enter password
        
        
        #------------------------- write players to excel sheet --------------------#
        df = pd.DataFrame(positions,players[1:])
        df.reset_index(inplace=True)
        df.columns = ["Player","Pos" ]    
        
        ax = pd.DataFrame({"Player" :names, "Action" : actions})
        
        tix = pd.DataFrame(tactics)
        tix.columns=["Tactics"]

        roles = pd.DataFrame(roles)
        roles.columns=["Role"]

        formations = {"Formation": [formation]}
        fo = pd.DataFrame(formations)
        
        with pd.ExcelWriter("Weekly Submissions/Weekly Yth Sub.xlsx") as writer:
            df.to_excel(writer, sheet_name="ft",index=True)
            tix.to_excel(writer, sheet_name="tactics",index=True)
            roles.to_excel(writer, sheet_name="roles",index=True)
            ax.to_excel(writer, sheet_name="actions",index=True)
            fo.to_excel(writer, sheet_name="formations",index=True)
            subs.to_excel(writer, sheet_name="subs",index=True)

    
# ================================================== ENABLE SUBMIT BUTTONS ================================================== #

    def enable_first_submit(self):
        for frame in self.frames.values():
            if isinstance(frame, (First)):
                frame.enable_first_submit()
                
    def enable_res_submit(self):
        for frame in self.frames.values():
            if isinstance(frame, (Reserves)):
                frame.enable_res_submit()



# ## First Team Class

# In[3]:


# ======================================================================================================================= #  
# =================================================== FIRST TEAM ======================================================== #
# ======================================================================================================================= #  
class First(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.configure(fg_color="gray14")

        # =========== CANVAS ============= #

        # Configure grid weights for expansion
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Canvas and Scrollbar
        canvas = ctk.CTkCanvas(self, bg="gray14")
        canvas.grid(row=2, column=0, columnspan=5, rowspan=5, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(self, hover=True, command=canvas.yview)
        scrollbar.grid(row=2, column=3, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Inner frame to hold the content
        self.scrollable_frame = ctk.CTkFrame(canvas, fg_color="gray14")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Add the inner frame to the canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def on_mousewheel(event):
            shift = (event.state & 0x1) != 0
            scroll = -1 if event.delta > 0 else 1
            if shift:
                canvas.xview_scroll(scroll, "units")
            else:
                canvas.yview_scroll(scroll, "units")

        canvas.bind("<MouseWheel>", on_mousewheel)
        
        # ============== STYLE =============== #

        # This will create style object
        style = ttk.Style()

        # Label style
        style.configure('Label', font=('Helvetica', 12), foreground='white', background="#719bb7")
        # checkbox style
        style.configure("TCheckbutton", indicatorbackground="black", indicatorforeground="white",
                        background="lightblue", foreground="black")

        # Title
        title = ctk.CTkLabel(self, text="First Team", font=('Helvetica', 20))
        title.grid(row=0, column=0, pady=10, padx=10)

        # Reserve button
        button1 = ctk.CTkButton(self.scrollable_frame, text="Reserves", width=100, fg_color="#0b6974", hover_color="#547588",
                                command=lambda: controller.show_frame(Reserves))
        button1.grid(row=1, column=1, pady=5, padx=5)

        # Youth button
        button2 = ctk.CTkButton(self.scrollable_frame, text="Youths", width=100, fg_color="#0b6974", hover_color="#547588",
                                command=lambda: controller.show_frame(Youths))
        button2.grid(row=1, column=2, pady=5, padx=5)
        
        # Set file paths to pull team details from
        file = "Turn Data/Show Team.xlsx"
        file2 = "Weekly Submissions/Weekly Sub.xlsx"
        # Get pandas dataframes
        global gks, deff, mid, att, DFA, last_player, last_pos
        gks = pd.read_excel(open(file, "rb"), sheet_name="gks")
        deff = pd.read_excel(open(file, "rb"), sheet_name="deff")
        mid = pd.read_excel(open(file, "rb"), sheet_name="mid")
        att = pd.read_excel(open(file, "rb"), sheet_name="att")
        DFA = pd.concat([deff, mid, att])


        # concat a list of all players IDs and Names only - for roles and training
        gks2r = gks.copy()
        gks2r.drop(list(gks2r.filter(regex='Unna')), axis=1, inplace=True)
        gks2r.drop(gks2r.iloc[:,2:],axis=1, inplace=True)
        gks2rlist = gks2r["Name"].tolist()
        deff2r = deff.copy()
        deff2r.drop(list(deff2r.filter(regex='Unna')), axis=1, inplace=True)
        deff2r.drop(deff2r.iloc[:,2:],axis=1, inplace=True)
        deff2rlist = deff2r["Name"].tolist()
        mid2r = mid.copy()
        mid2r.drop(list(mid2r.filter(regex='Unna')), axis=1, inplace=True)
        mid2r.drop(mid2r.iloc[:,2:],axis=1, inplace=True)
        mid2rlist = mid2r["Name"].tolist()
        att2r = att.copy()
        att2r.drop(list(att2r.filter(regex='Unna')), axis=1, inplace=True)
        att2r.drop(att2r.iloc[:,2:],axis=1, inplace=True)
        att2rlist = att2r["Name"].tolist()
        roles_list = gks2rlist+deff2rlist+mid2rlist+att2rlist
        roles_df = pd.concat([gks2r,deff2r,mid2r,att2r]) # make dataframe of name and ID
        roles_list # make list of names only

        # get last week's names
        last = pd.read_excel(file2)
        last_player = last.Player.tolist()
        last_pos = last.Pos.tolist()
        
        # ============ set positional lists ============ #
        deff_pos = ["LB","CB","SW","RB","LWB","RWB"]; 
        mid_pos = ["CM","AM","FR","PL","LM","RM"]; 
        att_pos = ["CF","TM","IF","LF","RF"]
        all_pos = [""] + deff_pos + mid_pos + att_pos
        
        # ============ set player lists ============ #
        GK_names = gks['Name'].tolist()
        Deff_names = deff['Name'].tolist() 
        Mid_names = mid['Name'].tolist() 
        Att_names = att['Name'].tolist() 
        all_players = [""] + GK_names + Deff_names + Mid_names + Att_names
        
        # ============ Drop Down Variables ============ #
        PL1 = StringVar(); PL2 = StringVar();PL3 = StringVar();PL4 = StringVar();PL5 = StringVar();PL6 = StringVar();PL7 = StringVar();PL8 = StringVar();PL9 = StringVar();PL10 = StringVar();PL11 = StringVar() # store player names
        Pos2 = StringVar();Pos3 = StringVar();Pos4 = StringVar();Pos5 = StringVar();Pos6 = StringVar();Pos7 = StringVar();Pos8 = StringVar();Pos9 = StringVar();Pos10 = StringVar();Pos11 = StringVar()  # store positions
        sub1 = StringVar();sub2 = StringVar();sub3 = StringVar();sub4 = StringVar();sub5 = StringVar() # store sub names

        team_select = ctk.CTkLabel(self.scrollable_frame, text='Team Selection', text_color="white", font=("Helvetica", 14))
        team_select.grid(row=2, column=1, pady=10)
        
        #------------- GK drop downs --------------#
        GK_txt = ctk.CTkLabel(self.scrollable_frame, text='Goalkeeper', text_color="white", font=("Helvetica", 12))
        GK_txt.grid(row=5, column=1, pady=(10,0), padx=0)
        PL1_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL1, values=GK_names)
        PL1.set(GK_names[0])
        PL1_btn.grid(row=5, column=2, pady=(10,0), padx=0) # button to choose GK

        
        #------------- Defender drop downs --------------#
        P2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 1',text_color="white", font=("Helvetica",12)); P2_txt.grid(row=6,column=1,padx=0,pady=(4,0))
        PL2_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL2, values=Deff_names); PL2.set(last_player[0]); PL2_button.grid(row=6,column=2,pady=(4,0)); # button to choose player 2
        Pos2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); Pos2_txt.grid(row=6,column=3,pady=(4,0))
        PL2_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos2, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos2.set(last_pos[0]); PL2_pos.grid(row=6,column=4,pady=(4,0)); # button to choose player position 2
        
        P3_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 2',text_color="white", font=("Helvetica",12)); P3_txt.grid(row=7,column=1,pady=(4,0))
        PL3_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL3, values=Deff_names); PL3.set(last_player[1]); PL3_button.grid(row=7,column=2,pady=(4,0)) # player 3 btn
        PL3_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos3, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos3.set(last_pos[1]); PL3_pos.grid(row=7,column=4,pady=(4,0)); # button to choose player position 3
        
        P4_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 3',text_color="white", font=("Helvetica",12)); P4_txt.grid(row=8,column=1,pady=(4,0))
        PL4_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL4, values=Deff_names); PL4.set(last_player[2]); PL4_button.grid(row=8,column=2,pady=(4,0))
        PL4_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos4, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos4.set(last_pos[2]); PL4_pos.grid(row=8,column=4,pady=(4,0)); # player position 4
        
        P5_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 4',text_color="white", font=("Helvetica",12)); P5_txt.grid(row=9,column=1,pady=(4,0))
        PL5_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL5, values=Deff_names); PL5.set(last_player[3]); PL5_button.grid(row=9,column=2,pady=(4,0))
        PL5_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos5, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos5.set(last_pos[3]); PL5_pos.grid(row=9,column=4,pady=(4,0)); # player position 5

        #------------- Midfielder drop downs --------------#
        P6_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 1',text_color="white", font=("Helvetica",12)); P6_txt.grid(row=10,column=1,padx=0,pady=(4,0))
        PL6_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL6, values=Mid_names); PL6.set(last_player[4]); PL6_button.grid(row=10,column=2,pady=(4,0))
        Pos6_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); Pos6_txt.grid(row=10,column=3,pady=(4,0))
        PL6_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos6, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos6.set(last_pos[4]); PL6_pos.grid(row=10,column=4,pady=(4,0)); # player position 6
        
        P7_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 2',text_color="white", font=("Helvetica",12)); P7_txt.grid(row=11,column=1,pady=(4,0))
        PL7_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL7, values=Mid_names); PL7.set(last_player[5]); PL7_button.grid(row=11,column=2,pady=(4,0))
        PL7_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos7, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos7.set(last_pos[5]); PL7_pos.grid(row=11,column=4,pady=(4,0)); # player position 7
        
        P8_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 3',text_color="white", font=("Helvetica",12)); P8_txt.grid(row=12,column=1,pady=(4,0))
        PL8_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL8, values=Mid_names); PL8.set(last_player[6]); PL8_button.grid(row=12,column=2,pady=(4,0))
        PL8_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos8, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos8.set(last_pos[6]); PL8_pos.grid(row=12,column=4,pady=(4,0)); # player position 8
        
        P9_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 4',text_color="white", font=("Helvetica",12)); P9_txt.grid(row=13,column=1,pady=(4,0))
        PL9_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL9, values=Mid_names); PL9.set(last_player[7]); PL9_button.grid(row=13,column=2,pady=(4,0))
        PL9_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos9, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos9.set(last_pos[7]); PL9_pos.grid(row=13,column=4,pady=(4,0)); # player position 9
        
        
        #------------- Attacker drop downs --------------#
        P10_txt = ctk.CTkLabel(self.scrollable_frame,text ='Attacker 1',text_color="white", font=("Helvetica",12)); P10_txt.grid(row=14,column=1,padx=0,pady=(4,0))
        PL10_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL10, values=Att_names); PL10.set(last_player[8]); PL10_button.grid(row=14,column=2,pady=(4,0))
        Pos10_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); Pos10_txt.grid(row=14,column=3,pady=(4,0))
        PL10_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos10, width=70, values=att_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos10.set(last_pos[8]); PL10_pos.grid(row=14,column=4,pady=(4,0)); # player position 10
        
        P11_txt = ctk.CTkLabel(self.scrollable_frame,text ='Attacker 2',text_color="white", font=("Helvetica",12)); P11_txt.grid(row=15,column=1,pady=(4,0))
        PL11_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL11, values=Att_names); PL11.set(last_player[9]); PL11_button.grid(row=15,column=2,pady=(4,0))
        PL11_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos11, width=70, values=att_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos11.set(last_pos[9]); PL11_pos.grid(row=15,column=4,pady=(4,0)); # player position 11
        
        
        #------------- Substitute drop downs --------------#
        sub1_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 1',text_color="white", font=("Helvetica",12)); sub1_txt.grid(row=16,column=1,padx=0,pady=(4,0))
        sub1_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub1 ,values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); 
        sub1_button.grid(row=16,column=2,pady=(4,0)); sub1.set(last_player[10]);
        
        sub2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 2',text_color="white", font=("Helvetica",12)); sub2_txt.grid(row=17,column=1)
        sub2_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub2, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); 
        sub2_button.grid(row=17,column=2,pady=(4,0)); sub2.set(last_player[11]);

        sub3_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 3',text_color="white", font=("Helvetica",12)); sub3_txt.grid(row=18,column=1)
        sub3_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub3, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); 
        sub3_button.grid(row=18,column=2,pady=(4,0)); sub3.set(last_player[12]);
        
        sub4_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 4',text_color="white", font=("Helvetica",12)); sub4_txt.grid(row=19,column=1)
        sub4_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub4, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); 
        sub4_button.grid(row=19,column=2,pady=(4,0)); sub4.set(last_player[13])
        
        sub5_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 5',text_color="white", font=("Helvetica",12)); sub5_txt.grid(row=20,column=1)
        sub5_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub5, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); 
        sub5_button.grid(row=20,column=2,pady=(4,0)); sub5.set(last_player[14])

        
        # ================= TACTICS ================= #
        tactics = pd.read_excel(open(file2,"rb"), sheet_name="tactics")
        tix = tactics.Tactics.tolist()
        #tactic variables
        tac1=StringVar();tac2=StringVar();tac3=StringVar();tac4=StringVar();tac5=StringVar();tac6=StringVar();mstr=StringVar()
        deff_tacs = ["DD","MM","GIH","ZD","POD","OST"]
        mid_tacs = ["PP","KP","AOB","PTW","FM","SD"]
        att_tacs = ["SOS","CS","RAD","LP","AB","DFF"]
        master_tac = [""] + deff_tacs + mid_tacs + att_tacs
        #tac_btn1
        tac_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Def Tac 1');  tac_txt1.grid(row=6,column=5)
        tac_btn1 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac1, values=deff_tacs, width=75); tac1.set(tix[0]); tac_btn1.grid(row=6,column=6)
        #tac_btn2
        tac_txt2 = ctk.CTkLabel(self.scrollable_frame,text ='Def Tac 2'); tac_txt2.grid(row=7,column=5)
        tac_btn2 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac2, values=deff_tacs, width=75); tac2.set(tix[1]); tac_btn2.grid(row=7,column=6)
                #tac_btn2
        tac_txt3 = ctk.CTkLabel(self.scrollable_frame,text ='Mid Tac 1'); tac_txt3.grid(row=8,column=5)
        tac_btn3 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac3, values=mid_tacs, width=75); tac3.set(tix[2]); tac_btn3.grid(row=8,column=6)
                #tac_btn2
        tac_txt4 = ctk.CTkLabel(self.scrollable_frame,text ='Mid Tac 2'); tac_txt4.grid(row=9,column=5)
        tac_btn4 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac4, values=mid_tacs, width=75); tac4.set(tix[3]); tac_btn4.grid(row=9,column=6)
                #tac_btn2
        tac_txt5 = ctk.CTkLabel(self.scrollable_frame,text ='Att Tac 1'); tac_txt5.grid(row=10,column=5)
        tac_btn5 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac5, values=att_tacs, width=75); tac5.set(tix[4]); tac_btn5.grid(row=10,column=6)
                #tac_btn2
        tac_txt6 = ctk.CTkLabel(self.scrollable_frame,text ='Att Tac 2'); tac_txt6.grid(row=11,column=5)
        tac_btn6 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac6, values=att_tacs, width=75); tac6.set(tix[5]); tac_btn6.grid(row=11,column=6)
                #tac_btn2
        mstr_txt = ctk.CTkLabel(self.scrollable_frame,text ='Master'); mstr_txt.grid(row=12,column=5)
        mstr_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=mstr, values=master_tac, width=75); mstr.set(tix[6]); mstr_btn.grid(row=12,column=6)

        # ================= ROLES ================= #
        cpt=StringVar();frk=StringVar();pen=StringVar()
        roles_prev = pd.read_excel(open(file2,"rb"), sheet_name="roles")
        roles_prev.drop(list(roles_prev.filter(regex='Unna')), axis=1, inplace=True)
        rr = roles_prev.Role.tolist()
        if len(rr) < 1:
            rr = ("Choose","Choose","Choose")
        else:
            pass
                
        cpt_txt = ctk.CTkLabel(self.scrollable_frame,text ='Captain'); cpt_txt.grid(row=14,column=5)
        cpt_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=cpt, values=roles_list, width=100); cpt.set(rr[0]); cpt_btn.grid(row=14,column=6)
        
        frk_txt = ctk.CTkLabel(self.scrollable_frame,text ='Freekicks'); frk_txt.grid(row=15,column=5)
        frk_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=frk, values=roles_list, width=100); frk.set(rr[1]); frk_btn.grid(row=15,column=6)
        
        pen_txt = ctk.CTkLabel(self.scrollable_frame,text ='Penalties'); pen_txt.grid(row=16,column=5)
        pen_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=pen, values=roles_list, width=100); pen.set(rr[2]); pen_btn.grid(row=16,column=6) 

        
        # ================= CUP OPTIONS ================= #
        sub_opt1 = IntVar(); sub_opt2 = IntVar()
        Chck1_txt = ctk.CTkLabel(self.scrollable_frame,text ='Same team and tactics as league?'); Chck1_txt.grid(row=18,column=8, columnspan=2)
        Chck1 = ctk.CTkCheckBox(self.scrollable_frame, text="", height=3,width=3, variable=sub_opt1, onvalue=1, offvalue=0); Chck1.grid(row=18, column=7)

        
        Chck2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Same sub options as league?'); Chck2_txt.grid(row=19,column=8, columnspan=2)
        Chck2 = ctk.CTkCheckBox(self.scrollable_frame, text="", height=3,width=3, variable=sub_opt2, onvalue=1, offvalue=0); Chck2.grid(row=19,column=7)

        
        # ================= TRAINING ================= #
        train1=StringVar();train2=StringVar();train3=StringVar();train4=StringVar();train5=StringVar();train6=StringVar();train7=StringVar();train8=StringVar();train9=StringVar();train10=StringVar()
        
        training_hours = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25"]
            
        # get last week's submitted training
        train_prev = pd.read_excel(open(file2,"rb"), sheet_name="training")
        tp = train_prev.Training.tolist()
        
        #training btn 1
        tra_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Study Opp (L)');  tra_txt1.grid(row=6,column=8)
        tra_btn1 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train1, values=training_hours, width=75); train1.set(tp[0]); tra_btn1.grid(row=6,column=9)
        #training btn 2
        tra_txt2 = ctk.CTkLabel(self.scrollable_frame,text ='Study Opp (C)');  tra_txt2.grid(row=7,column=8)
        tra_btn2 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train2, values=training_hours, width=75); train2.set(tp[1]); tra_btn2.grid(row=7,column=9)
        #training btn 3
        tra_txt3 = ctk.CTkLabel(self.scrollable_frame,text ='Passing');  tra_txt3.grid(row=8,column=8)
        tra_btn3 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train3, values=training_hours, width=75); train3.set(tp[2]); tra_btn3.grid(row=8,column=9)
        #training btn 4
        tra_txt4 = ctk.CTkLabel(self.scrollable_frame,text ='Ballskills');  tra_txt4.grid(row=9,column=8)
        tra_btn4 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train4, values=training_hours, width=75); train4.set(tp[3]); tra_btn4.grid(row=9,column=9)
        #training btn 5
        tra_txt5 = ctk.CTkLabel(self.scrollable_frame,text ='Defensive');  tra_txt5.grid(row=10,column=8)
        tra_btn5 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train5, values=training_hours, width=75); train5.set(tp[4]); tra_btn5.grid(row=10,column=9)
        #training btn 6
        tra_txt6 = ctk.CTkLabel(self.scrollable_frame,text ='Attacking');  tra_txt6.grid(row=11,column=8)
        tra_btn6 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train6, values=training_hours, width=75); train6.set(tp[5]); tra_btn6.grid(row=11,column=9)
        #training btn 7
        tra_txt7 = ctk.CTkLabel(self.scrollable_frame,text ='Heading');  tra_txt7.grid(row=12,column=8)
        tra_btn7 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train7, values=training_hours, width=75); train7.set(tp[6]); tra_btn7.grid(row=12,column=9)
        #training btn 8
        tra_txt8 = ctk.CTkLabel(self.scrollable_frame,text ='Five a sides');  tra_txt8.grid(row=13,column=8)
        tra_btn8 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train8, values=training_hours, width=75); train8.set(tp[7]); tra_btn8.grid(row=13,column=9)
        #training btn 9
        tra_txt9 = ctk.CTkLabel(self.scrollable_frame,text ='Fitness');  tra_txt9.grid(row=14,column=8)
        tra_btn9 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train9, values=training_hours, width=75); train9.set(tp[8]); tra_btn9.grid(row=14,column=9)
        #training btn 10
        tra_txt10 = ctk.CTkLabel(self.scrollable_frame,text ='Strength');  tra_txt10.grid(row=15,column=8)
        tra_btn10 = ctk.CTkOptionMenu(self.scrollable_frame, variable=train10, values=training_hours, width=75); train10.set(tp[9]); tra_btn10.grid(row=15,column=9)

        # Define a function to safely convert values to integers
        def safe_int(value):
            try:
                return int(value)
            except ValueError:
                return ""
        
        # ================= SUBSTITUTES =============== #
        prev_subs = pd.read_excel(open(file2,"rb"), sheet_name="subs")
        prev_subs.drop(list(prev_subs.filter(regex='Unna')), axis=1, inplace=True)
        prev_subs = prev_subs.fillna("")
        prev_circ = prev_subs.Circumstance.tolist()
        prev_on = prev_subs["Player On"].tolist()
        prev_off = prev_subs["Player Off"].tolist()
        prev_pos = prev_subs.Position.tolist()
        
        # Initialize an empty list to store the variables
        mins = []
        
        # Iterate over the 'Minute' column in prev_subs and convert to integers
        for item in prev_subs['Minute']:
            if isinstance(item, (int, float)):  # Check if it's a numeric value
                mins.append(int(item))  # Convert to int if it's numeric
            else:
                mins.append("")  # Append empty string if not numeric
        
        sub1_min=StringVar();sub2_min=StringVar();sub3_min=StringVar();sub4_min=StringVar();sub5_min=StringVar();
        sub1_circ=StringVar();sub2_circ=StringVar();sub3_circ=StringVar();sub4_circ=StringVar();sub5_circ=StringVar();
        sub1_on=StringVar();sub2_on=StringVar();sub3_on=StringVar();sub4_on=StringVar();sub5_on=StringVar();
        sub1_off=StringVar();sub2_off=StringVar();sub3_off=StringVar();sub4_off=StringVar();sub5_off=StringVar();
        sub1_pos=StringVar();sub2_pos=StringVar();sub3_pos=StringVar();sub4_pos=StringVar();sub5_pos=StringVar();

        circumstances = ["","Any","Winning","Drawing","Losing", "Not Winning", "Not Losing", "Not Drawing"]
        
        #row 22 for 7 rows + 1 row for space
        sub_opt_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub Options',text_color="white", font=("Helvetica",14)); sub_opt_txt.grid(row=22,column=1, pady=10)

        sub_id_txt = ctk.CTkLabel(self.scrollable_frame,text ='Minute',text_color="white", font=("Helvetica",12)); sub_id_txt.grid(row=23,column=1, pady=5)
        sub_con_txt = ctk.CTkLabel(self.scrollable_frame,text ='Circumstance',text_color="white", font=("Helvetica",12)); sub_con_txt.grid(row=23,column=2, pady=5)
        sub_on_txt = ctk.CTkLabel(self.scrollable_frame,text ='Player On',text_color="white", font=("Helvetica",12)); sub_on_txt.grid(row=23,column=3, pady=5)
        sub_off_txt = ctk.CTkLabel(self.scrollable_frame,text ='Player Off',text_color="white", font=("Helvetica",12)); sub_off_txt.grid(row=23,column=4, pady=5)
        sub_pos_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); sub_pos_txt.grid(row=23,column=5, pady=5)

        
        sub1_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub1_min, width=60);  sub1_min.set(mins[0]); sub1_time.grid(row=24,column=1,padx=2,pady=2)
        sub1_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub1_circ, values=circumstances, width=120); sub1_con.set(prev_circ[0]); sub1_con.grid(row=24,column=2,padx=2,pady=2)
        sub1_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub1_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub1_pl_on.set(prev_on[0]); sub1_pl_on.grid(row=24,column=3,padx=2,pady=2)
        sub1_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub1_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub1_pl_off.set(prev_off[0]);  sub1_pl_off.grid(row=24,column=4,padx=2,pady=2)
        sub1_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub1_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub1_role.set(prev_pos[0]);  sub1_role.grid(row=24,column=5,padx=2,pady=2)
        
        sub2_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub2_min, width=60);  sub2_min.set(mins[1]); sub2_time.grid(row=25,column=1,padx=2,pady=2)
        sub2_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub2_circ, values=circumstances, width=120); sub2_con.set(prev_circ[1]); sub2_con.grid(row=25,column=2,padx=2,pady=2)
        sub2_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub2_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub2_pl_on.set(prev_on[1]); sub2_pl_on.grid(row=25,column=3,padx=2,pady=2)
        sub2_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub2_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub2_pl_off.set(prev_off[1]);  sub2_pl_off.grid(row=25,column=4,padx=2,pady=2)
        sub2_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub2_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283");  sub2_role.set(prev_pos[1]); sub2_role.grid(row=25,column=5,padx=2,pady=2)
        
        sub3_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub3_min, width=60); sub3_min.set(mins[2]); sub3_time.grid(row=26,column=1,padx=2,pady=2)
        sub3_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub3_circ, values=circumstances, width=120); sub3_con.set(prev_circ[2]); sub3_con.grid(row=26,column=2,padx=2,pady=2)
        sub3_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub3_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub3_pl_on.set(prev_on[2]); sub3_pl_on.grid(row=26,column=3,padx=2,pady=2)
        sub3_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub3_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub3_pl_off.set(prev_off[2]);  sub3_pl_off.grid(row=26,column=4,padx=2,pady=2)
        sub3_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub3_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub3_role.set(prev_pos[2]);  sub3_role.grid(row=26,column=5,padx=2,pady=2)
        
        sub4_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub4_min, width=60); sub4_min.set(mins[3]);  sub4_time.grid(row=27,column=1,padx=2,pady=2)
        sub4_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub4_circ, values=circumstances, width=120); sub4_con.set(prev_circ[3]); sub4_con.grid(row=27,column=2,padx=2,pady=2)
        sub4_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub4_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub4_pl_on.set(prev_on[3]); sub4_pl_on.grid(row=27,column=3,padx=2,pady=2)
        sub4_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub4_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub4_pl_off.set(prev_off[3]);  sub4_pl_off.grid(row=27,column=4,padx=2,pady=2)
        sub4_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub4_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub4_role.set(prev_pos[3]);   sub4_role.grid(row=27,column=5,padx=2,pady=2)

        sub5_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub5_min, width=60); sub5_min.set(mins[4]);  sub5_time.grid(row=28,column=1,padx=2,pady=2)
        sub5_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub5_circ, values=circumstances, width=120); sub5_con.set(prev_circ[4]); sub5_con.grid(row=28,column=2,padx=2,pady=2)
        sub5_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub5_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub5_pl_on.set(prev_on[4]);  sub5_pl_on.grid(row=28,column=3,padx=2,pady=2)
        sub5_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub5_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub5_pl_off.set(prev_off[4]);  sub5_pl_off.grid(row=28,column=4,padx=2,pady=2)
        sub5_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub5_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub5_role.set(prev_pos[4]);  sub5_role.grid(row=28,column=5,padx=2,pady=2)
        
        # ================= ACTIONS ================= #
        name1=StringVar();name2=StringVar();name3=StringVar();name4=StringVar();name5=StringVar();name6=StringVar();name7=StringVar();name8=StringVar();name9=StringVar();name10=StringVar();
        action1=StringVar();action2=StringVar();action3=StringVar();action4=StringVar();action5=StringVar();action6=StringVar();action7=StringVar();action8=StringVar();action9=StringVar();action10=StringVar()
        SPS1=StringVar();SPS2=StringVar();
        actions = pd.read_csv("Actions/G124.csv").set_index("ID")
        actions_list = actions["TEA Random"].tolist()
        actions_list.insert(0,"")
        roles_list.insert(0,"")
        # get last week's submitted actions
        actions_prev = pd.read_excel(open(file2,"rb"), sheet_name="actions")
        np = actions_prev.fillna("").Player.tolist()
        ap = actions_prev.fillna("").Action.tolist()

        # title
        action_txt = ctk.CTkLabel(self.scrollable_frame,text ='Actions',text_color="white", font=("Helvetica",14)); action_txt.grid(row=30,column=1, pady=10)

        #action btn 1
        act_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Name');  act_txt1.grid(row=31,column=1, padx=5,pady=(4,0))
        act_btn1 = ctk.CTkComboBox(self.scrollable_frame, variable=name1, values=roles_list); act_btn1.grid(row=31,column=2); name1.set(np[0]);
        lst_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Action');  lst_txt1.grid(row=31,column=3,padx=2.5)
        list1 = ctk.CTkComboBox(self.scrollable_frame, variable=action1); action1.set(ap[0]); list1.grid(row=31,column=4);
        plact_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='SPS');  plact_txt1.grid(row=31,column=5,padx=2.5)
        plact1 = ctk.CTkEntry(self.scrollable_frame, textvariable=SPS1);  plact1.grid(row=31,column=6,padx=2.5)
        #action btn 2
        act_btn2 = ctk.CTkComboBox(self.scrollable_frame, variable=name2, values=roles_list); act_btn2.grid(row=32,column=2); name2.set(np[1]);
        list2 = ctk.CTkComboBox(self.scrollable_frame, variable=action2); action2.set(ap[1]); list2.grid(row=32,column=4);
        plact2 = ctk.CTkEntry(self.scrollable_frame, textvariable=SPS2);  plact2.grid(row=32,column=6,padx=2.5)
        #action btn 3
        act_btn3 = ctk.CTkComboBox(self.scrollable_frame, variable=name3, values=roles_list); act_btn3.grid(row=33,column=2); name3.set(np[2]);
        list3 = ctk.CTkComboBox(self.scrollable_frame, variable=action3); action3.set(ap[2]); list3.grid(row=33,column=4);
        plact3 = ctk.CTkEntry(self.scrollable_frame);  plact3.grid(row=33,column=6,padx=2.5)
        #action btn 4
        act_btn4 = ctk.CTkComboBox(self.scrollable_frame, variable=name4, values=roles_list); act_btn4.grid(row=34,column=2); name4.set(np[3]);
        list4 = ctk.CTkComboBox(self.scrollable_frame, variable=action4); action4.set(ap[3]); list4.grid(row=34,column=4);
        plact4 = ctk.CTkEntry(self.scrollable_frame);  plact4.grid(row=34,column=6,padx=2.5)
        #action btn 5
        act_btn5 = ctk.CTkComboBox(self.scrollable_frame, variable=name5,  values=roles_list); act_btn5.grid(row=35,column=2); name5.set(np[4]);
        list5 = ctk.CTkComboBox(self.scrollable_frame, variable=action5); action5.set(ap[4]); list5.grid(row=35,column=4); 
        plact5 = ctk.CTkEntry(self.scrollable_frame);  plact5.grid(row=35,column=6,padx=2.5)
        #action btn 6
        act_btn6 = ctk.CTkComboBox(self.scrollable_frame, variable=name6,  values=roles_list); act_btn6.grid(row=36,column=2); name6.set(np[5]);
        list6 = ctk.CTkComboBox(self.scrollable_frame,variable=action6); action6.set(ap[5]); list6.grid(row=36,column=4);
        plact6 = ctk.CTkEntry(self.scrollable_frame);  plact6.grid(row=36,column=6,padx=2.5)
        #action btn 7
        act_btn7 = ctk.CTkComboBox(self.scrollable_frame, variable=name7, values=roles_list); act_btn7.grid(row=37,column=2); name7.set(np[6]);
        list7 = ctk.CTkComboBox(self.scrollable_frame, variable=action7); action7.set(ap[6]); list7.grid(row=37,column=4);
        plact7 = ctk.CTkEntry(self.scrollable_frame);  plact7.grid(row=37,column=6,padx=2.5)
        #action btn 8
        act_btn8 = ctk.CTkComboBox(self.scrollable_frame, variable=name8, values=roles_list); act_btn8.grid(row=38,column=2); name8.set(np[7]);
        list8 = ctk.CTkComboBox(self.scrollable_frame, variable=action8); action8.set(ap[7]); list8.grid(row=38,column=4);
        plact8 = ctk.CTkEntry(self.scrollable_frame);  plact8.grid(row=38,column=6,padx=2.5)
        #action btn 9
        act_btn9 = ctk.CTkComboBox(self.scrollable_frame, variable=name9, values=roles_list); act_btn9.grid(row=39,column=2); name9.set(np[8]);
        list9 = ctk.CTkComboBox(self.scrollable_frame, variable=action9); action9.set(ap[8]); list9.grid(row=39,column=4);
        plact9 = ctk.CTkEntry(self.scrollable_frame);  plact9.grid(row=39,column=6,padx=2.5)
        #action btn 10
        act_btn10 = ctk.CTkComboBox(self.scrollable_frame, variable=name10, values=roles_list); act_btn10.grid(row=40,column=2); name10.set(np[9]);
        list10 = ctk.CTkComboBox(self.scrollable_frame, variable=action10); action10.set(ap[9]); list10.grid(row=40,column=4);
        plact10 = ctk.CTkEntry(self.scrollable_frame);  plact10.grid(row=40,column=6,padx=2.5)
        
        CTkScrollableDropdown(list1, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action1.set(e),list1.set(e)))
        CTkScrollableDropdown(list2, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action2.set(e),list2.set(e)))
        CTkScrollableDropdown(list3, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action3.set(e),list3.set(e)))
        CTkScrollableDropdown(list4, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action4.set(e),list4.set(e)))
        CTkScrollableDropdown(list5, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action5.set(e),list5.set(e)))
        CTkScrollableDropdown(list6, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action6.set(e),list6.set(e)))
        CTkScrollableDropdown(list7, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action7.set(e),list7.set(e)))
        CTkScrollableDropdown(list8, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action8.set(e),list8.set(e)))
        CTkScrollableDropdown(list9, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action9.set(e),list9.set(e)))
        CTkScrollableDropdown(list10, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action10.set(e),list10.set(e)))

        list1.set(ap[0])
        list2.set(ap[1])
        list3.set(ap[2])
        list4.set(ap[3])
        list5.set(ap[4])
        list6.set(ap[5])
        list7.set(ap[6])
        list8.set(ap[7])
        list9.set(ap[8])
        list10.set(ap[9])

        # ================= MESSAGE ================= #
        message = StringVar()
        message_txt =  ctk.CTkLabel(self.scrollable_frame,text ='Message')
        message_txt.grid(row=21,column=7)
        message_input = ctk.CTkEntry(self.scrollable_frame, width=350, textvariable=message)
        message_input.grid(row=21,column=8, columnspan=3)

        # ================= PASSWORD ================= #
        passwd = StringVar()
        passwd_txt = ctk.CTkLabel(self.scrollable_frame,text ='Password')
        passwd_txt.grid(row=22,column=7)
        passwd_input = ctk.CTkEntry(self.scrollable_frame, textvariable=passwd)
        passwd_input.grid(row=22,column=8)

        
        # ================= FORMATIONS ================= #
        Formation_txt =  ctk.CTkLabel(self.scrollable_frame,text="Formation: ",font=("Helvetica",16)).grid(row=2, column=6, padx=(10,0))
        global formation
        formation = pd.read_excel(open(file2,"rb"), sheet_name="formations")
        formation.drop(list(formation.filter(regex='Unna')), axis=1, inplace=True)
        formation = formation.squeeze()
        
        
        def five_four_one(self):
            global formation; formation = 541
            
             # Update PL6 to Deff
            PL6_button.configure(values=Deff_names)
            PL6_pos.configure(values=deff_pos)

            # Update PL10 to Att
            PL10_button.configure(values=Mid_names)
            PL10_pos.configure(values=mid_pos)

            P6_txt.configure(text="Defender 5") # Update label
            P7_txt.configure(text="Midfielder 1")
            P8_txt.configure(text="Midfielder 2")
            P9_txt.configure(text="Midfielder 3")
            P10_txt.configure(text="Midfielder 4")
            P11_txt.configure(text="Attacker 1")
            
            form_541.configure(state="disabled") # Disable the button
            form_532.configure(state="normal") # Disable the button
            form_442.configure(state="normal") # Disable the button
            form_451.configure(state="normal") # Disable the button
            
        # 541 button
        form_541 = ctk.CTkButton(self.scrollable_frame, text="541",  width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: five_four_one(self))
        form_541.grid(row=2, column=7)

        def five_three_two(self):
            global formation; formation = 532
            
             # Update PL6 to Deff
            PL6_button.configure(values=Deff_names)
            PL6_pos.configure(values=deff_pos)

            # Update PL10 to Att
            PL10_button.configure(values=Att_names)
            PL10_pos.configure(values=att_pos)
            
            P6_txt.configure(text="Defender 5") # Update label
            P7_txt.configure(text="Midfielder 1")
            P8_txt.configure(text="Midfielder 2")
            P9_txt.configure(text="Midfielder 3")               
            P10_txt.configure(text="Attacker 1")
            P11_txt.configure(text="Attacker 2")

            form_541.configure(state="normal") # Disable the button
            form_532.configure(state="disabled") # Disable the button
            form_442.configure(state="normal") # Disable the button
            form_451.configure(state="normal") # Disable the button
            
        # 532 button
        form_532 = ctk.CTkButton(self.scrollable_frame, text="532",  width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: five_three_two(self))
        form_532.grid(row=2, column=8)

        def four_four_two(self):
            global formation; formation = 442
            
             # Update PL6 to Mid
            PL6_button.configure(values=Mid_names)
            PL6_pos.configure(values=mid_pos)

            # Update PL10 to Att
            PL10_button.configure(values=Att_names)
            PL10_pos.configure(values=att_pos)

            P6_txt.configure(text="Midfielder 1") # Update label
            P7_txt.configure(text="Midfielder 2")
            P8_txt.configure(text="Midfielder 3")
            P9_txt.configure(text="Midfielder 4")               
            P10_txt.configure(text="Attacker 1")
            P11_txt.configure(text="Attacker 2")
            
            form_541.configure(state="normal") # Disable the button
            form_532.configure(state="normal") # Disable the button
            form_442.configure(state="disabled") # Disable the button
            form_451.configure(state="normal") # Disable the button
            
        # 442 button
        form_442 = ctk.CTkButton(self.scrollable_frame, text="442",  width=100,  fg_color="#0b6974", hover_color="#547588", command=lambda: four_four_two(self))
        form_442.grid(row=2, column=9)

        def four_five_one(self):
            global formation
            formation = 451
       
            # Update PL6 with Mid_names
            PL6_button.configure(values=Mid_names)
            PL6_pos.configure(values=mid_pos)

            # Update PL6 with Mid_names
            PL10_button.configure(values=Mid_names)
            PL10_pos.configure(values=mid_pos)
            
            # Update labels
            P6_txt.configure(text="Midfielder 1")
            P7_txt.configure(text="Midfielder 2")
            P8_txt.configure(text="Midfielder 3")
            P9_txt.configure(text="Midfielder 4")
            P10_txt.configure(text="Midfielder 5")
            P11_txt.configure(text="Attacker 1")
        
            # Disable/Enable buttons
            form_541.configure(state="normal")
            form_532.configure(state="normal")
            form_442.configure(state="normal")
            form_451.configure(state="disabled")
            
        # 442 button
        form_451 = ctk.CTkButton(self.scrollable_frame, text="451", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: four_five_one(self))
        form_451.grid(row=2, column=10)

        if formation == 442:
            four_four_two(self)
        elif formation == 532:
            five_three_two(self)
        elif formation == 541:
            five_four_one(self)
        elif formation == 451:
            four_five_one(self)
        else:
            pass
            
        # ============================================ #
        # ================= GET INFO ================= #
        # ============================================ #
        def set_first_team(self):
            # make tuple of players and positions to pass to the submit function
            self.players = (PL1.get(), PL2.get(), PL3.get(), PL4.get(), PL5.get(), PL6.get(), PL7.get(), PL8.get(), PL9.get(), PL10.get(), PL11.get(), sub1.get(), sub2.get(), sub3.get(), sub4.get(), sub5.get())
            self.positions = (Pos2.get(), Pos3.get(), Pos4.get(), Pos5.get(), Pos6.get(), Pos7.get(), Pos8.get(), Pos9.get(), Pos10.get(), Pos11.get(), "sub1", "sub2", "sub3", "sub4", "sub5")
            self.tactics = (tac1.get(),tac2.get(),tac3.get(),tac4.get(),tac5.get(),tac6.get(),mstr.get())
            self.roles = (cpt.get(),frk.get(),pen.get())
            self.roles_df = roles_df
            self.ticks = (sub_opt1.get(),sub_opt2.get())
            self.training = (train1.get(),train2.get(),train3.get(),train4.get(),train5.get(),train6.get(),train7.get(),train8.get(),train9.get(),train10.get())
            self.names = (name1.get(),name2.get(),name3.get(),name4.get(),name5.get(),name6.get(),name7.get(),name8.get(),name9.get(),name10.get())
            self.actions = (action1.get(),action2.get(),action3.get(),action4.get(),action5.get(),action6.get(),action7.get(),action8.get(),action9.get(),action10.get())
            self.submit_button.configure(state="normal")
            self.password = passwd.get()
            self.message = message.get()
            self.substitute_options = {
                "Minute": [sub1_min.get(),sub2_min.get(),sub3_min.get(),sub4_min.get(),sub5_min.get()],
                "Circumstance" : [sub1_circ.get(),sub2_circ.get(),sub3_circ.get(),sub4_circ.get(),sub5_circ.get()],
                "Player On" : [sub1_on.get(),sub2_on.get(),sub3_on.get(),sub4_on.get(),sub5_on.get()],
                "Player Off" : [sub1_off.get(),sub2_off.get(),sub3_off.get(),sub4_off.get(),sub5_off.get()],
                "Position" : [sub1_pos.get(),sub2_pos.get(),sub3_pos.get(),sub4_pos.get(),sub5_pos.get()]
            }
            self.subs = pd.DataFrame(self.substitute_options)
            self.SPS = (SPS1.get(),SPS2.get())
            #print(f"{self.players},\n{self.positions,self.tactics,self.roles} \nNames: {self.names} \nActions: {self.actions} \nFormation = {formation}\nSPS = {self.SPS}")
            #print(f'Password entered is "{self.password}"')
            
        # set button
        set_btn = ctk.CTkButton(self.scrollable_frame, text="Set First Team", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: set_first_team(self)) # set button
        set_btn.grid(row=1, column=4,pady=10, padx=10)
        
        # ================= SUBMIT ================= #
        self.submit_button = ctk.CTkButton(self.scrollable_frame, text="Submit", width=100, fg_color="#7c1645", hover_color="#30a56c", command=lambda: self.controller.submit_first_team(self.players,self.positions,self.tactics,self.roles,self.roles_df,
                                                                                                                                                                        self.ticks,self.training,self.actions,self.names,self.password,
                                                                                                                                                                        formation,self.message, self.SPS, self.subs))
        self.submit_button.configure(state=DISABLED)
        self.submit_button.grid(row=1, column=3,pady=10, padx=10)

        
# =================================== FIRST TEAM ====================================== #


# ## Reserves Class

# In[4]:


# =================================== RESERVES ====================================== #
class Reserves(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.configure(fg_color="gray14")

        # =========== CANVAS ============= #

        # Configure grid weights for expansion
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Canvas and Scrollbar
        canvas2 = ctk.CTkCanvas(self, bg="gray14")
        canvas2.grid(row=2, column=0, columnspan=5, rowspan=5, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(self, hover=True, command=canvas2.yview)
        scrollbar.grid(row=2, column=3, sticky="ns")

        canvas2.configure(yscrollcommand=scrollbar.set)

        # Inner frame to hold the content
        self.scrollable_frame = ctk.CTkFrame(canvas2, fg_color="gray14")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas2.configure(
                scrollregion=canvas2.bbox("all")
            )
        )

        # Add the inner frame to the canvas
        canvas2.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # ============== STYLE =============== #

        # Title
        title = ctk.CTkLabel(self, text="Res Team", font = ('Helvetica', 20))
        title.grid(row=0, column=0,pady=10, padx=10)
        
        # reserve button
        button1 = ctk.CTkButton(self.scrollable_frame, text="First Team", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: controller.show_frame(First))
        button1.grid(row=1, column=1, pady=5,padx=5)

        # youth button
        button2 = ctk.CTkButton(self.scrollable_frame, text="Youths", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: controller.show_frame(Youths))
        button2.grid(row=1, column=2, pady=5,padx=5)

        # set filepaths to pull team details from
        file = "Turn Data/Show Team.xlsx"
        file2 = "Weekly Submissions/Weekly Res Sub.xlsx"
        # get pd dfs
        global gks, deff, mid, att, DFA, last_player, last_pos
        gks = pd.read_excel(open(file,"rb"), sheet_name="r_gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="r_deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="r_mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="r_att")
        DFA = pd.concat([deff,mid,att])

        # Load the data during application startup
        actions = pd.read_csv("Actions/Res_actions.csv").set_index("ID")
        actions_list = actions["TEA Random"].tolist()
        actions_list.insert(0, "")
        

       # concat a list of all players IDs and Names only - for roles and training
        gks2r = gks.copy()
        gks2r.drop(list(gks2r.filter(regex='Unna')), axis=1, inplace=True)
        gks2r.drop(gks2r.iloc[:,2:],axis=1, inplace=True)
        gks2rlist = gks2r["Name"].tolist()
        deff2r = deff.copy()
        deff2r.drop(list(deff2r.filter(regex='Unna')), axis=1, inplace=True)
        deff2r.drop(deff2r.iloc[:,2:],axis=1, inplace=True)
        deff2rlist = deff2r["Name"].tolist()
        mid2r = mid.copy()
        mid2r.drop(list(mid2r.filter(regex='Unna')), axis=1, inplace=True)
        mid2r.drop(mid2r.iloc[:,2:],axis=1, inplace=True)
        mid2rlist = mid2r["Name"].tolist()
        att2r = att.copy()
        att2r.drop(list(att2r.filter(regex='Unna')), axis=1, inplace=True)
        att2r.drop(att2r.iloc[:,2:],axis=1, inplace=True)
        att2rlist = att2r["Name"].tolist()
        roles_list = gks2rlist+deff2rlist+mid2rlist+att2rlist
        roles_df = pd.concat([gks2r,deff2r,mid2r,att2r]) # make dataframe of name and ID
        roles_list # make list of names only


        # get last week's names
        last = pd.read_excel(file2)
        last_player = last.Player.tolist()
        last_pos = last.Pos.tolist()
        
        # ============ set positional lists ============ #
        deff_pos = ["LB","CB","SW","RB","LWB","RWB"]; 
        mid_pos = ["CM","AM","FR","PL","LM","RM"]; 
        att_pos = ["CF","TM","IF","LF","RF"]
        all_pos = [""] + deff_pos + mid_pos + att_pos
        
        # ============ set player lists ============ #
        GK_names = gks['Name'].tolist();
        Deff_names = deff['Name'].tolist(); 
        Mid_names = mid['Name'].tolist(); 
        Att_names = att['Name'].tolist(); 
        all_players = GK_names + Deff_names + Mid_names + Att_names
        
         # ============ Drop Down Variables ============ #
        PL1 = StringVar(); PL2 = StringVar(); PL3 = StringVar(); PL4 = StringVar(); PL5 = StringVar(); PL6 = StringVar(); PL7 = StringVar(); PL8 = StringVar(); PL9 = StringVar(); PL10 = StringVar(); PL11 = StringVar() # store player names
        Pos2 = StringVar(); Pos3 = StringVar(); Pos4 = StringVar(); Pos5 = StringVar(); Pos6 = StringVar(); Pos7 = StringVar(); Pos8 = StringVar(); Pos9 = StringVar();Pos10 = StringVar(); Pos11 = StringVar()  # store positions
        sub1 = StringVar(); sub2 = StringVar();sub3 = StringVar();sub4 = StringVar();sub5 = StringVar(); # store sub names

        team_select = ctk.CTkLabel(self.scrollable_frame,text ='Team Selection',text_color="white", font=("Helvetica",14)); team_select.grid(row=2,column=1, pady=10)
        
        #------------- GK drop downs --------------#
        GK_txt = ctk.CTkLabel(self.scrollable_frame,text ='Goalkeeper',text_color="white", font=("Helvetica",12)); GK_txt.grid(row=5, column=1,pady=(10,0), padx=0)
        PL1_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL1, values=GK_names); PL1.set(GK_names[0]);PL1_btn.grid(row=5, column=2,pady=(10,0), padx=0) # button to choose GK

        
        #------------- Defender drop downs --------------#
        P2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 1',text_color="white", font=("Helvetica",12)); P2_txt.grid(row=6,column=1,padx=0,pady=(4,0))
        PL2_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL2, values=Deff_names); PL2.set(last_player[0]); PL2_button.grid(row=6,column=2,pady=(4,0)); # button to choose player 2
        Pos2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); Pos2_txt.grid(row=6,column=3,pady=(4,0))
        PL2_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos2, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos2.set(last_pos[0]); PL2_pos.grid(row=6,column=4,pady=(4,0)); # button to choose player position 2
        
        P3_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 2',text_color="white", font=("Helvetica",12)); P3_txt.grid(row=7,column=1,pady=(4,0))
        PL3_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL3, values=Deff_names); PL3.set(last_player[1]); PL3_button.grid(row=7,column=2,pady=(4,0)) # player 3 btn
        PL3_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos3, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos3.set(last_pos[1]); PL3_pos.grid(row=7,column=4,pady=(4,0)); # button to choose player position 3
        
        P4_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 3',text_color="white", font=("Helvetica",12)); P4_txt.grid(row=8,column=1,pady=(4,0))
        PL4_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL4, values=Deff_names); PL4.set(last_player[2]); PL4_button.grid(row=8,column=2,pady=(4,0))
        PL4_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos4, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos4.set(last_pos[2]); PL4_pos.grid(row=8,column=4,pady=(4,0)); # player position 4
        
        P5_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 4',text_color="white", font=("Helvetica",12)); P5_txt.grid(row=9,column=1,pady=(4,0))
        PL5_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL5, values=Deff_names); PL5.set(last_player[3]); PL5_button.grid(row=9,column=2,pady=(4,0))
        PL5_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos5, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos5.set(last_pos[3]); PL5_pos.grid(row=9,column=4,pady=(4,0)); # player position 5

        #------------- Midfielder drop downs --------------#
        P6_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 1',text_color="white", font=("Helvetica",12)); P6_txt.grid(row=10,column=1,padx=0,pady=(4,0))
        PL6_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL6, values=Mid_names); PL6.set(last_player[4]); PL6_button.grid(row=10,column=2,pady=(4,0))
        Pos6_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); Pos6_txt.grid(row=10,column=3,pady=(10,0))
        PL6_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos6, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos6.set(last_pos[4]); PL6_pos.grid(row=10,column=4,pady=(4,0)); # player position 6
        
        P7_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 2',text_color="white", font=("Helvetica",12)); P7_txt.grid(row=11,column=1,pady=(4,0))
        PL7_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL7, values=Mid_names); PL7.set(last_player[5]); PL7_button.grid(row=11,column=2,pady=(4,0))
        PL7_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos7, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos7.set(last_pos[5]); PL7_pos.grid(row=11,column=4,pady=(4,0)); # player position 7
        
        P8_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 3',text_color="white", font=("Helvetica",12)); P8_txt.grid(row=12,column=1,pady=(4,0))
        PL8_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL8, values=Mid_names); PL8.set(last_player[6]); PL8_button.grid(row=12,column=2,pady=(4,0))
        PL8_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos8, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos8.set(last_pos[6]); PL8_pos.grid(row=12,column=4,pady=(4,0)); # player position 8
        
        P9_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 4',text_color="white", font=("Helvetica",12)); P9_txt.grid(row=13,column=1,pady=(4,0))
        PL9_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL9, values=Mid_names); PL9.set(last_player[7]); PL9_button.grid(row=13,column=2,pady=(4,0))
        PL9_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos9, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos9.set(last_pos[7]); PL9_pos.grid(row=13,column=4,pady=(4,0)); # player position 9
        
        
        #------------- Attacker drop downs --------------#
        P10_txt = ctk.CTkLabel(self.scrollable_frame,text ='Attacker 1',text_color="white", font=("Helvetica",12)); P10_txt.grid(row=14,column=1,padx=0,pady=(4,0))
        PL10_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL10, values=Att_names); PL10.set(last_player[8]); PL10_button.grid(row=14,column=2,pady=(4,0))
        Pos10_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); Pos10_txt.grid(row=14,column=3,pady=(4,0))
        PL10_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos10, width=70, values=att_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos10.set(last_pos[8]); PL10_pos.grid(row=14,column=4,pady=(4,0)); # player position 10
        
        P11_txt = ctk.CTkLabel(self.scrollable_frame,text ='Attacker 2',text_color="white", font=("Helvetica",12)); P11_txt.grid(row=15,column=1,pady=(4,0))
        PL11_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL11, values=Att_names); PL11.set(last_player[9]); PL11_button.grid(row=15,column=2,pady=(4,0))
        PL11_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos11, width=70, values=att_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos11.set(last_pos[9]); PL11_pos.grid(row=15,column=4,pady=(4,0)); # player position 11
        
           
        
        #------------- Substitute drop downs --------------#
        sub1_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 1',text_color="white", font=("Helvetica",12)); sub1_txt.grid(row=16,column=1,padx=0,pady=(4,0))
        sub1_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub1 ,values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub1_button.grid(row=16,column=2,pady=(4,0)); sub1.set(last_player[10]);
        
        sub2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 2',text_color="white", font=("Helvetica",12)); sub2_txt.grid(row=17,column=1)
        sub2_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub2, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub2_button.grid(row=17,column=2,pady=(4,0)); sub2.set(last_player[11]);

        sub3_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 3',text_color="white", font=("Helvetica",12)); sub3_txt.grid(row=18,column=1)
        sub3_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub3, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub3_button.grid(row=18,column=2,pady=(4,0)); sub3.set(last_player[12]);
        
        sub4_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 4',text_color="white", font=("Helvetica",12)); sub4_txt.grid(row=19,column=1)
        sub4_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub4, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub4_button.grid(row=19,column=2,pady=(4,0)); sub4.set(last_player[13])
        
        sub5_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 5',text_color="white", font=("Helvetica",12)); sub5_txt.grid(row=20,column=1)
        sub5_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub5, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub5_button.grid(row=20,column=2,pady=(4,0)); sub5.set(last_player[14])
        
        # ================= TACTICS ================= #
        tactics = pd.read_excel(open(file2,"rb"), sheet_name="tactics")
        tix = tactics.Tactics.tolist()
        #tactic variables
        tac1=StringVar();tac2=StringVar();tac3=StringVar();tac4=StringVar();tac5=StringVar();tac6=StringVar();mstr=StringVar()
        deff_tacs = ["DD","MM","GIH","ZD","POD","OST"]
        mid_tacs = ["PP","KP","AOB","PTW","FM","SD"]
        att_tacs = ["SOS","CS","RAD","LP","AB","DFF"]
        master_tac = [""] + deff_tacs + mid_tacs + att_tacs
        #tac_btn1
        tac_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Def Tac 1');  tac_txt1.grid(row=6,column=5)
        tac_btn1 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac1, values=deff_tacs, width=75); tac1.set(tix[0]); tac_btn1.grid(row=6,column=6)
        #tac_btn2
        tac_txt2 = ctk.CTkLabel(self.scrollable_frame,text ='Def Tac 2'); tac_txt2.grid(row=7,column=5)
        tac_btn2 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac2, values=deff_tacs, width=75); tac2.set(tix[1]); tac_btn2.grid(row=7,column=6)
                #tac_btn2
        tac_txt3 = ctk.CTkLabel(self.scrollable_frame,text ='Mid Tac 1'); tac_txt3.grid(row=8,column=5)
        tac_btn3 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac3, values=mid_tacs, width=75); tac3.set(tix[2]); tac_btn3.grid(row=8,column=6)
                #tac_btn2
        tac_txt4 = ctk.CTkLabel(self.scrollable_frame,text ='Mid Tac 2'); tac_txt4.grid(row=9,column=5)
        tac_btn4 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac4, values=mid_tacs, width=75); tac4.set(tix[3]); tac_btn4.grid(row=9,column=6)
                #tac_btn2
        tac_txt5 = ctk.CTkLabel(self.scrollable_frame,text ='Att Tac 1'); tac_txt5.grid(row=10,column=5)
        tac_btn5 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac5, values=att_tacs, width=75); tac5.set(tix[4]); tac_btn5.grid(row=10,column=6)
                #tac_btn2
        tac_txt6 = ctk.CTkLabel(self.scrollable_frame,text ='Att Tac 2'); tac_txt6.grid(row=11,column=5)
        tac_btn6 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac6, values=att_tacs, width=75); tac6.set(tix[5]); tac_btn6.grid(row=11,column=6)
                #tac_btn2
        mstr_txt = ctk.CTkLabel(self.scrollable_frame,text ='Master'); mstr_txt.grid(row=12,column=5)
        mstr_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=mstr, values=master_tac, width=75); mstr.set(tix[6]); mstr_btn.grid(row=12,column=6)

        # ================= ROLES ================= #
        cpt=StringVar();frk=StringVar();pen=StringVar()
        roles_prev = pd.read_excel(open(file2,"rb"), sheet_name="roles")
        roles_prev.drop(list(roles_prev.filter(regex='Unna')), axis=1, inplace=True)
        rr = roles_prev.Role.tolist()
        if len(rr) < 1:
            rr = ("Choose","Choose","Choose")
        else:
            pass
                
        cpt_txt = ctk.CTkLabel(self.scrollable_frame,text ='Captain'); cpt_txt.grid(row=14,column=5)
        cpt_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=cpt, values=roles_list, width=100); cpt.set(rr[0]); cpt_btn.grid(row=14,column=6)
        
        frk_txt = ctk.CTkLabel(self.scrollable_frame,text ='Freekicks'); frk_txt.grid(row=15,column=5)
        frk_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=frk, values=roles_list, width=100); frk.set(rr[1]); frk_btn.grid(row=15,column=6)
        
        pen_txt = ctk.CTkLabel(self.scrollable_frame,text ='Penalties'); pen_txt.grid(row=16,column=5)
        pen_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=pen, values=roles_list, width=100); pen.set(rr[2]); pen_btn.grid(row=16,column=6) 

        # ================= SUBSTITUTES =============== #
        prev_subs = pd.read_excel(open(file2,"rb"), sheet_name="subs")
        prev_subs.drop(list(prev_subs.filter(regex='Unna')), axis=1, inplace=True)
        prev_subs = prev_subs.fillna("")
        prev_circ = prev_subs.Circumstance.tolist()
        prev_on = prev_subs["Player On"].tolist()
        prev_off = prev_subs["Player Off"].tolist()
        prev_pos = prev_subs.Position.tolist()
        
        # Initialize an empty list to store the variables
        mins = []
        
        # Iterate over the 'Minute' column in prev_subs and convert to integers
        for item in prev_subs['Minute']:
            if isinstance(item, (int, float)):  # Check if it's a numeric value
                mins.append(int(item))  # Convert to int if it's numeric
            else:
                mins.append("")  # Append empty string if not numeric
        
        sub1_min=StringVar();sub2_min=StringVar();sub3_min=StringVar();sub4_min=StringVar();sub5_min=StringVar();
        sub1_circ=StringVar();sub2_circ=StringVar();sub3_circ=StringVar();sub4_circ=StringVar();sub5_circ=StringVar();
        sub1_on=StringVar();sub2_on=StringVar();sub3_on=StringVar();sub4_on=StringVar();sub5_on=StringVar();
        sub1_off=StringVar();sub2_off=StringVar();sub3_off=StringVar();sub4_off=StringVar();sub5_off=StringVar();
        sub1_pos=StringVar();sub2_pos=StringVar();sub3_pos=StringVar();sub4_pos=StringVar();sub5_pos=StringVar();

        circumstances = ["","Any","Winning","Drawing","Losing", "Not Winning", "Not Losing", "Not Drawing"]
        
        #row 22 for 7 rows + 1 row for space
        sub_opt_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub Options',text_color="white", font=("Helvetica",14)); sub_opt_txt.grid(row=22,column=1, pady=10)

        sub_id_txt = ctk.CTkLabel(self.scrollable_frame,text ='Minute',text_color="white", font=("Helvetica",12)); sub_id_txt.grid(row=23,column=1, pady=5)
        sub_con_txt = ctk.CTkLabel(self.scrollable_frame,text ='Circumstance',text_color="white", font=("Helvetica",12)); sub_con_txt.grid(row=23,column=2, pady=5)
        sub_on_txt = ctk.CTkLabel(self.scrollable_frame,text ='Player On',text_color="white", font=("Helvetica",12)); sub_on_txt.grid(row=23,column=3, pady=5)
        sub_off_txt = ctk.CTkLabel(self.scrollable_frame,text ='Player Off',text_color="white", font=("Helvetica",12)); sub_off_txt.grid(row=23,column=4, pady=5)
        sub_pos_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); sub_pos_txt.grid(row=23,column=5, pady=5)

        
        sub1_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub1_min, width=60);  sub1_min.set(mins[0]); sub1_time.grid(row=24,column=1,padx=2,pady=2)
        sub1_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub1_circ, values=circumstances, width=120); sub1_con.set(prev_circ[0]); sub1_con.grid(row=24,column=2,padx=2,pady=2)
        sub1_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub1_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub1_pl_on.set(prev_on[0]); sub1_pl_on.grid(row=24,column=3,padx=2,pady=2)
        sub1_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub1_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub1_pl_off.set(prev_off[0]);  sub1_pl_off.grid(row=24,column=4,padx=2,pady=2)
        sub1_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub1_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub1_role.set(prev_pos[0]);  sub1_role.grid(row=24,column=5,padx=2,pady=2)
        
        sub2_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub2_min, width=60);  sub2_min.set(mins[1]); sub2_time.grid(row=25,column=1,padx=2,pady=2)
        sub2_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub2_circ, values=circumstances, width=120); sub2_con.set(prev_circ[1]); sub2_con.grid(row=25,column=2,padx=2,pady=2)
        sub2_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub2_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub2_pl_on.set(prev_on[1]); sub2_pl_on.grid(row=25,column=3,padx=2,pady=2)
        sub2_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub2_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub2_pl_off.set(prev_off[1]);  sub2_pl_off.grid(row=25,column=4,padx=2,pady=2)
        sub2_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub2_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283");  sub2_role.set(prev_pos[1]); sub2_role.grid(row=25,column=5,padx=2,pady=2)
        
        sub3_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub3_min, width=60); sub3_min.set(mins[2]); sub3_time.grid(row=26,column=1,padx=2,pady=2)
        sub3_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub3_circ, values=circumstances, width=120); sub3_con.set(prev_circ[2]); sub3_con.grid(row=26,column=2,padx=2,pady=2)
        sub3_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub3_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub3_pl_on.set(prev_on[2]); sub3_pl_on.grid(row=26,column=3,padx=2,pady=2)
        sub3_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub3_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub3_pl_off.set(prev_off[2]);  sub3_pl_off.grid(row=26,column=4,padx=2,pady=2)
        sub3_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub3_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub3_role.set(prev_pos[2]);  sub3_role.grid(row=26,column=5,padx=2,pady=2)
        
        sub4_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub4_min, width=60); sub4_min.set(mins[3]);  sub4_time.grid(row=27,column=1,padx=2,pady=2)
        sub4_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub4_circ, values=circumstances, width=120); sub4_con.set(prev_circ[3]); sub4_con.grid(row=27,column=2,padx=2,pady=2)
        sub4_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub4_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub4_pl_on.set(prev_on[3]); sub4_pl_on.grid(row=27,column=3,padx=2,pady=2)
        sub4_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub4_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub4_pl_off.set(prev_off[3]);  sub4_pl_off.grid(row=27,column=4,padx=2,pady=2)
        sub4_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub4_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub4_role.set(prev_pos[3]);   sub4_role.grid(row=27,column=5,padx=2,pady=2)

        sub5_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub5_min, width=60); sub5_min.set(mins[4]);  sub5_time.grid(row=28,column=1,padx=2,pady=2)
        sub5_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub5_circ, values=circumstances, width=120); sub5_con.set(prev_circ[4]); sub5_con.grid(row=28,column=2,padx=2,pady=2)
        sub5_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub5_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub5_pl_on.set(prev_on[4]);  sub5_pl_on.grid(row=28,column=3,padx=2,pady=2)
        sub5_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub5_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub5_pl_off.set(prev_off[4]);  sub5_pl_off.grid(row=28,column=4,padx=2,pady=2)
        sub5_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub5_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub5_role.set(prev_pos[4]);  sub5_role.grid(row=28,column=5,padx=2,pady=2)
        

        # ================= ACTIONS ================= #
        name1=StringVar();name2=StringVar();name3=StringVar();name4=StringVar();name5=StringVar()
        action1=StringVar();action2=StringVar();action3=StringVar();action4=StringVar();action5=StringVar()
        roles_list.insert(0,"")
        # get last week's submitted actions
        actions_prev = pd.read_excel(open(file2,"rb"), sheet_name="actions")
        np = actions_prev.Player.fillna("").tolist()
        ap = actions_prev.Action.fillna("").tolist()

        action_txt = ctk.CTkLabel(self.scrollable_frame,text ='Actions',text_color="white", font=("Helvetica",14)); action_txt.grid(row=30,column=1, pady=10)
        
        #action btn 1
        act_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Name');  act_txt1.grid(row=31,column=1, padx=5,pady=(4,0))
        act_btn1 = ctk.CTkComboBox(self.scrollable_frame, variable=name1, values=roles_list); act_btn1.grid(row=31,column=2); name1.set(np[0]);
        lst_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Action');  lst_txt1.grid(row=31,column=3,padx=2.5)
        list1 = ctk.CTkComboBox(self.scrollable_frame, variable=action1); action1.set(ap[0]); list1.grid(row=31,column=4);
        
        #action btn 2
        act_btn2 = ctk.CTkComboBox(self.scrollable_frame, variable=name2, values=roles_list); act_btn2.grid(row=32,column=2); name2.set(np[1]);
        list2 = ctk.CTkComboBox(self.scrollable_frame, variable=action2); action2.set(ap[1]); list2.grid(row=32,column=4);

        #action btn 3
        act_btn3 = ctk.CTkComboBox(self.scrollable_frame, variable=name3, values=roles_list); act_btn3.grid(row=33,column=2); name3.set(np[2]);
        list3 = ctk.CTkComboBox(self.scrollable_frame, variable=action3); action3.set(ap[2]); list3.grid(row=33,column=4);

        #action btn 4
        act_btn4 = ctk.CTkComboBox(self.scrollable_frame, variable=name4, values=roles_list); act_btn4.grid(row=34,column=2); name4.set(np[3]);
        list4 = ctk.CTkComboBox(self.scrollable_frame, variable=action4); action4.set(ap[3]); list4.grid(row=34,column=4);

        #action btn 5
        act_btn5 = ctk.CTkComboBox(self.scrollable_frame, variable=name5,  values=roles_list); act_btn5.grid(row=35,column=2); name5.set(np[4]);
        list5 = ctk.CTkComboBox(self.scrollable_frame, variable=action5); action5.set(ap[4]); list5.grid(row=35,column=4); 
 
        CTkScrollableDropdown(list1, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action1.set(e),list1.set(e)))
        CTkScrollableDropdown(list2, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action2.set(e),list2.set(e)))
        CTkScrollableDropdown(list3, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action3.set(e),list3.set(e)))
        CTkScrollableDropdown(list4, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action4.set(e),list4.set(e)))
        CTkScrollableDropdown(list5, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action5.set(e),list5.set(e)))

        list1.set(ap[0])
        list2.set(ap[1])
        list3.set(ap[2])
        list4.set(ap[3])
        list5.set(ap[4])        

        
        # ================= PASSWORD ================= #
        passwd = StringVar()
        passwd_txt = ctk.CTkLabel(self.scrollable_frame,text ='Password')
        passwd_txt.grid(row=21,column=7)
        passwd_input = passwd_input = ctk.CTkEntry(self.scrollable_frame, textvariable=passwd)
        passwd_input.grid(row=21,column=8,columnspan=4)

        
        # ================= FORMATIONS ================= #
        Formation_txt =  ctk.CTkLabel(self.scrollable_frame,text="Formation: ",font=("Helvetica",16)).grid(row=2, column=6, padx=(10,0))
        global formation
        formation = pd.read_excel(open(file2,"rb"), sheet_name="formations")
        formation.drop(list(formation.filter(regex='Unna')), axis=1, inplace=True)
        formation = formation.squeeze()
        
        def five_four_one(self):
            global formation; formation = 541
            
             # Update PL6 to Deff
            PL6_button.configure(values=Deff_names)
            PL6_pos.configure(values=deff_pos)

            # Update PL10 to Att
            PL10_button.configure(values=Mid_names)
            PL10_pos.configure(values=mid_pos)

            P6_txt.configure(text="Defender 5") # Update label
            P7_txt.configure(text="Midfielder 1")
            P8_txt.configure(text="Midfielder 2")
            P9_txt.configure(text="Midfielder 3")
            P10_txt.configure(text="Midfielder 4")
            P11_txt.configure(text="Attacker 1")
            
            form_541.configure(state="disabled") # Disable the button
            form_532.configure(state="normal") # Disable the button
            form_442.configure(state="normal") # Disable the button
            form_451.configure(state="normal") # Disable the button
            
        # 541 button
        form_541 = ctk.CTkButton(self.scrollable_frame, text="541", width=80, fg_color="#0b6974", hover_color="#547588", command=lambda: five_four_one(self))
        form_541.grid(row=2, column=7)

        def five_three_two(self):
            global formation; formation = 532
            
             # Update PL6 to Deff
            PL6_button.configure(values=Deff_names)
            PL6_pos.configure(values=deff_pos)

            # Update PL10 to Att
            PL10_button.configure(values=Att_names)
            PL10_pos.configure(values=att_pos)
            
            P6_txt.configure(text="Defender 5") # Update label
            P7_txt.configure(text="Midfielder 1")
            P8_txt.configure(text="Midfielder 2")
            P9_txt.configure(text="Midfielder 3")               
            P10_txt.configure(text="Attacker 1")
            P11_txt.configure(text="Attacker 2")

            form_541.configure(state="normal") # Disable the button
            form_532.configure(state="disabled") # Disable the button
            form_442.configure(state="normal") # Disable the button
            form_451.configure(state="normal") # Disable the button
            
        # 532 button
        form_532 = ctk.CTkButton(self.scrollable_frame, text="532", width=80, fg_color="#0b6974", hover_color="#547588", command=lambda: five_three_two(self))
        form_532.grid(row=2, column=8)

        def four_four_two(self):
            global formation; formation = 442
            
             # Update PL6 to Mid
            PL6_button.configure(values=Mid_names)
            PL6_pos.configure(values=mid_pos)

            # Update PL10 to Att
            PL10_button.configure(values=Att_names)
            PL10_pos.configure(values=att_pos)

            P6_txt.configure(text="Midfielder 1") # Update label
            P7_txt.configure(text="Midfielder 2")
            P8_txt.configure(text="Midfielder 3")
            P9_txt.configure(text="Midfielder 4")               
            P10_txt.configure(text="Attacker 1")
            P11_txt.configure(text="Attacker 2")
            
            form_541.configure(state="normal") # Disable the button
            form_532.configure(state="normal") # Disable the button
            form_442.configure(state="disabled") # Disable the button
            form_451.configure(state="normal") # Disable the button
            
        # 442 button
        form_442 = ctk.CTkButton(self.scrollable_frame, text="442", width=80, fg_color="#0b6974", hover_color="#547588", command=lambda: four_four_two(self))
        form_442.grid(row=2, column=9)

        def four_five_one(self):
            global formation
            formation = 451
            print(formation)
        
            # Update PL6 with Mid_names
            PL6_button.configure(values=Mid_names)
            PL6_pos.configure(values=mid_pos)

            # Update PL6 with Mid_names
            PL10_button.configure(values=Mid_names)
            PL10_pos.configure(values=mid_pos)
            
            # Update labels
            P6_txt.configure(text="Midfielder 1")
            P7_txt.configure(text="Midfielder 2")
            P8_txt.configure(text="Midfielder 3")
            P9_txt.configure(text="Midfielder 4")
            P10_txt.configure(text="Midfielder 5")
            P11_txt.configure(text="Attacker 1")
        
            # Disable/Enable buttons
            form_541.configure(state="normal")
            form_532.configure(state="normal")
            form_442.configure(state="normal")
            form_451.configure(state="disabled")
            
        # 442 button
        form_451 = ctk.CTkButton(self.scrollable_frame, text="451", width=80, fg_color="#0b6974", hover_color="#547588", command=lambda: four_five_one(self))
        form_451.grid(row=2, column=10, padx=(2,0))

        if formation == 442:
            four_four_two(self)
        elif formation == 532:
            five_three_two(self)
        elif formation == 541:
            five_four_one(self)
        elif formation == 451:
            four_five_one(self)
        else:
            pass

        # ============================================ #
        # ================= GET INFO ================= #
        # ============================================ #
        def set_res_team(self):
            # make tuple of players and positions to pass to the submit function
            self.players = (PL1.get(), PL2.get(), PL3.get(), PL4.get(), PL5.get(), PL6.get(), PL7.get(), PL8.get(), PL9.get(), PL10.get(), PL11.get(), sub1.get(), sub2.get(), sub3.get(), sub4.get(), sub5.get())
            self.positions = (Pos2.get(), Pos3.get(), Pos4.get(), Pos5.get(), Pos6.get(), Pos7.get(), Pos8.get(), Pos9.get(), Pos10.get(), Pos11.get(), "sub1", "sub2", "sub3", "sub4", "sub5")
            self.tactics = (tac1.get(),tac2.get(),tac3.get(),tac4.get(),tac5.get(),tac6.get(),mstr.get())
            self.roles = (cpt.get(),frk.get(),pen.get())
            self.roles_df = roles_df
            self.names = (name1.get(),name2.get(),name3.get(),name4.get(),name5.get())
            self.actions = (action1.get(),action2.get(),action3.get(),action4.get(),action5.get())
            self.password = passwd.get()
            self.substitute_options = {
                "Minute": [sub1_min.get(),sub2_min.get(),sub3_min.get(),sub4_min.get(),sub5_min.get()],
                "Circumstance" : [sub1_circ.get(),sub2_circ.get(),sub3_circ.get(),sub4_circ.get(),sub5_circ.get()],
                "Player On" : [sub1_on.get(),sub2_on.get(),sub3_on.get(),sub4_on.get(),sub5_on.get()],
                "Player Off" : [sub1_off.get(),sub2_off.get(),sub3_off.get(),sub4_off.get(),sub5_off.get()],
                "Position" : [sub1_pos.get(),sub2_pos.get(),sub3_pos.get(),sub4_pos.get(),sub5_pos.get()]
            }
            self.subs = pd.DataFrame(self.substitute_options)
            self.submit_button.configure(state="normal")
            
            print(f"{self.players},\n{self.positions,self.tactics,self.roles} \nNames: {self.names} \nActions: {self.actions} \nFormation = {formation}")
            print(f'Password entered is "{self.password}"')
            
        
        # set button
        set_btn = ctk.CTkButton(self.scrollable_frame, text="Set Res Team", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: set_res_team(self)) # set button
        set_btn.grid(row=1, column=4,pady=10, padx=10)


        # ================= SUBMIT ================= #
        self.submit_button = ctk.CTkButton(self.scrollable_frame, text="Submit", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: self.controller.submit_res_team(self.players,self.positions,
                                                                                                                                                                                       self.tactics,self.roles,self.roles_df,self.actions,
                                                                                                                                                                                       self.names,self.password,formation, self.subs))
        self.submit_button.configure(state=DISABLED)
        self.submit_button.grid(row=1, column=3,pady=10, padx=10)


# ## Youths Class

# In[5]:


# =================================== YOUTHS ====================================== #

class Youths(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.configure(fg_color="gray14")

        # =========== CANVAS ============= #

        # Configure grid weights for expansion
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Canvas and Scrollbar
        canvas = ctk.CTkCanvas(self, bg="gray14")
        canvas.grid(row=2, column=0, columnspan=5, rowspan=5, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(self, hover=True, command=canvas.yview)
        scrollbar.grid(row=2, column=3, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Inner frame to hold the content
        self.scrollable_frame = ctk.CTkFrame(canvas, fg_color="gray14")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Add the inner frame to the canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # ============== STYLE =============== #

        # Title
        title = ctk.CTkLabel(self, text="Youth Team", font = ('Helvetica', 20))
        title.grid(row=0, column=0,pady=10, padx=10)
        
        # reserve button
        button1 = ctk.CTkButton(self.scrollable_frame, text="First Team", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: controller.show_frame(First))
        button1.grid(row=1, column=1, pady=5,padx=5)

        # youth button
        button2 = ctk.CTkButton(self.scrollable_frame, text="Reserves", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: controller.show_frame(Reserves))
        button2.grid(row=1, column=2, pady=5,padx=5)


        # set filepaths to pull team details from
        file = "Turn Data/Show Team.xlsx"
        file2 = "Weekly Submissions/Weekly Yth Sub.xlsx"
        # get pd dfs
        global gks, deff, mid, att, DFA, last_player, last_pos
        gks = pd.read_excel(open(file,"rb"), sheet_name="y_gks")
        deff = pd.read_excel(open(file,"rb"), sheet_name="y_deff")
        mid = pd.read_excel(open(file,"rb"), sheet_name="y_mid")
        att = pd.read_excel(open(file,"rb"), sheet_name="y_att")
        DFA = pd.concat([deff,mid,att])


        # Load the data during application startup
        actions = pd.read_csv("Actions/Res_actions.csv").set_index("ID")
        actions_list = actions["TEA Random"].tolist()
        actions_list.insert(0, "")
        
       # concat a list of all players IDs and Names only - for roles and training
        gks2r = gks.copy()
        gks2r.drop(list(gks2r.filter(regex='Unna')), axis=1, inplace=True)
        gks2r.drop(gks2r.iloc[:,2:],axis=1, inplace=True)
        gks2rlist = gks2r["Name"].tolist()
        deff2r = deff.copy()
        deff2r.drop(list(deff2r.filter(regex='Unna')), axis=1, inplace=True)
        deff2r.drop(deff2r.iloc[:,2:],axis=1, inplace=True)
        deff2rlist = deff2r["Name"].tolist()
        mid2r = mid.copy()
        mid2r.drop(list(mid2r.filter(regex='Unna')), axis=1, inplace=True)
        mid2r.drop(mid2r.iloc[:,2:],axis=1, inplace=True)
        mid2rlist = mid2r["Name"].tolist()
        att2r = att.copy()
        att2r.drop(list(att2r.filter(regex='Unna')), axis=1, inplace=True)
        att2r.drop(att2r.iloc[:,2:],axis=1, inplace=True)
        att2rlist = att2r["Name"].tolist()
        roles_list = gks2rlist+deff2rlist+mid2rlist+att2rlist
        roles_df = pd.concat([gks2r,deff2r,mid2r,att2r]) # make dataframe of name and ID
        roles_list # make list of names only


        # get last week's names
        last = pd.read_excel(file2)
        last_player = last.Player.tolist()
        last_pos = last.Pos.tolist()
        
        # ============ set positional lists ============ #
        deff_pos = ["LB","CB","SW","RB","LWB","RWB"]; 
        mid_pos = ["CM","AM","FR","PL","LM","RM"]; 
        att_pos = ["CF","TM","IF","LF","RF"]
        all_pos = [""] + deff_pos + mid_pos + att_pos
        
        # ============ set player lists ============ #
        GK_names = gks['Name'].tolist();
        Deff_names = deff['Name'].tolist(); 
        Mid_names = mid['Name'].tolist(); 
        Att_names = att['Name'].tolist(); 
        all_players = GK_names + Deff_names + Mid_names + Att_names
        
        # ============ Drop Down Variables ============ #
        PL1 = StringVar(); PL2 = StringVar(); PL3 = StringVar(); PL4 = StringVar(); PL5 = StringVar(); PL6 = StringVar(); PL7 = StringVar(); PL8 = StringVar(); PL9 = StringVar(); PL10 = StringVar(); PL11 = StringVar() # store player names
        Pos2 = StringVar(); Pos3 = StringVar(); Pos4 = StringVar(); Pos5 = StringVar(); Pos6 = StringVar(); Pos7 = StringVar(); Pos8 = StringVar(); Pos9 = StringVar();Pos10 = StringVar(); Pos11 = StringVar()  # store positions
        sub1 = StringVar(); sub2 = StringVar();sub3 = StringVar();sub4 = StringVar();sub5 = StringVar(); # store sub names

        team_select = ctk.CTkLabel(self.scrollable_frame,text ='Team Selection',text_color="white", font=("Helvetica",14)); team_select.grid(row=2,column=1, pady=10)
        
        #------------- GK drop downs --------------#
        GK_txt = ctk.CTkLabel(self.scrollable_frame,text ='Goalkeeper',text_color="white", font=("Helvetica",12)); GK_txt.grid(row=5, column=1,pady=(10,0), padx=0)
        PL1_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL1, values=GK_names); PL1.set(GK_names[0]);PL1_btn.grid(row=5, column=2,pady=(10,0), padx=0) # button to choose GK

        
        #------------- Defender drop downs --------------#
        P2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 1',text_color="white", font=("Helvetica",12)); P2_txt.grid(row=6,column=1,padx=0,pady=(4,0))
        PL2_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL2, values=Deff_names); PL2.set(last_player[0]); PL2_button.grid(row=6,column=2,pady=(4,0)); # button to choose player 2
        Pos2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); Pos2_txt.grid(row=6,column=3,pady=(4,0))
        PL2_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos2, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos2.set(last_pos[0]); PL2_pos.grid(row=6,column=4,pady=(4,0)); # button to choose player position 2
        
        P3_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 2',text_color="white", font=("Helvetica",12)); P3_txt.grid(row=7,column=1,pady=(4,0))
        PL3_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL3, values=Deff_names); PL3.set(last_player[1]); PL3_button.grid(row=7,column=2,pady=(4,0)) # player 3 btn
        PL3_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos3, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos3.set(last_pos[1]); PL3_pos.grid(row=7,column=4,pady=(4,0)); # button to choose player position 3
        
        P4_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 3',text_color="white", font=("Helvetica",12)); P4_txt.grid(row=8,column=1,pady=(4,0))
        PL4_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL4, values=Deff_names); PL4.set(last_player[2]); PL4_button.grid(row=8,column=2,pady=(4,0))
        PL4_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos4, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos4.set(last_pos[2]); PL4_pos.grid(row=8,column=4,pady=(4,0)); # player position 4
        
        P5_txt = ctk.CTkLabel(self.scrollable_frame,text ='Defender 4',text_color="white", font=("Helvetica",12)); P5_txt.grid(row=9,column=1,pady=(4,0))
        PL5_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL5, values=Deff_names); PL5.set(last_player[3]); PL5_button.grid(row=9,column=2,pady=(4,0))
        PL5_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos5, width=70, values=deff_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos5.set(last_pos[3]); PL5_pos.grid(row=9,column=4,pady=(4,0)); # player position 5

        #------------- Midfielder drop downs --------------#
        P6_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 1',text_color="white", font=("Helvetica",12)); P6_txt.grid(row=10,column=1,padx=0,pady=(4,0))
        PL6_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL6, values=Mid_names); PL6.set(last_player[4]); PL6_button.grid(row=10,column=2,pady=(4,0))
        Pos6_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); Pos6_txt.grid(row=10,column=3,pady=(10,0))
        PL6_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos6, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos6.set(last_pos[4]); PL6_pos.grid(row=10,column=4,pady=(4,0)); # player position 6
        
        P7_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 2',text_color="white", font=("Helvetica",12)); P7_txt.grid(row=11,column=1,pady=(4,0))
        PL7_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL7, values=Mid_names); PL7.set(last_player[5]); PL7_button.grid(row=11,column=2,pady=(4,0))
        PL7_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos7, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos7.set(last_pos[5]); PL7_pos.grid(row=11,column=4,pady=(4,0)); # player position 7
        
        P8_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 3',text_color="white", font=("Helvetica",12)); P8_txt.grid(row=12,column=1,pady=(4,0))
        PL8_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL8, values=Mid_names); PL8.set(last_player[6]); PL8_button.grid(row=12,column=2,pady=(4,0))
        PL8_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos8, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos8.set(last_pos[6]); PL8_pos.grid(row=12,column=4,pady=(4,0)); # player position 8
        
        P9_txt = ctk.CTkLabel(self.scrollable_frame,text ='Midfielder 4',text_color="white", font=("Helvetica",12)); P9_txt.grid(row=13,column=1,pady=(4,0))
        PL9_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL9, values=Mid_names); PL9.set(last_player[7]); PL9_button.grid(row=13,column=2,pady=(4,0))
        PL9_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos9, width=70, values=mid_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos9.set(last_pos[7]); PL9_pos.grid(row=13,column=4,pady=(4,0)); # player position 9
        
        
        #------------- Attacker drop downs --------------#
        P10_txt = ctk.CTkLabel(self.scrollable_frame,text ='Attacker 1',text_color="white", font=("Helvetica",12)); P10_txt.grid(row=14,column=1,padx=0,pady=(4,0))
        PL10_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL10, values=Att_names); PL10.set(last_player[8]); PL10_button.grid(row=14,column=2,pady=(4,0))
        Pos10_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); Pos10_txt.grid(row=14,column=3,pady=(4,0))
        PL10_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos10, width=70, values=att_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos10.set(last_pos[8]); PL10_pos.grid(row=14,column=4,pady=(4,0)); # player position 10
        
        P11_txt = ctk.CTkLabel(self.scrollable_frame,text ='Attacker 2',text_color="white", font=("Helvetica",12)); P11_txt.grid(row=15,column=1,pady=(4,0))
        PL11_button = ctk.CTkOptionMenu(self.scrollable_frame, variable=PL11, values=Att_names); PL11.set(last_player[9]); PL11_button.grid(row=15,column=2,pady=(4,0))
        PL11_pos = ctk.CTkComboBox(self.scrollable_frame, variable=Pos11, width=70, values=att_pos, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); Pos11.set(last_pos[9]); PL11_pos.grid(row=15,column=4,pady=(4,0)); # player position 11
        
           
        
        #------------- Substitute drop downs --------------#
        sub1_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 1',text_color="white", font=("Helvetica",12)); sub1_txt.grid(row=16,column=1,padx=0,pady=(4,0))
        sub1_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub1 ,values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub1_button.grid(row=16,column=2,pady=(4,0)); sub1.set(last_player[10]);
        
        sub2_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 2',text_color="white", font=("Helvetica",12)); sub2_txt.grid(row=17,column=1)
        sub2_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub2, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub2_button.grid(row=17,column=2,pady=(4,0)); sub2.set(last_player[11]);

        sub3_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 3',text_color="white", font=("Helvetica",12)); sub3_txt.grid(row=18,column=1)
        sub3_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub3, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub3_button.grid(row=18,column=2,pady=(4,0)); sub3.set(last_player[12]);
        
        sub4_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 4',text_color="white", font=("Helvetica",12)); sub4_txt.grid(row=19,column=1)
        sub4_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub4, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub4_button.grid(row=19,column=2,pady=(4,0)); sub4.set(last_player[13])
        
        sub5_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub 5',text_color="white", font=("Helvetica",12)); sub5_txt.grid(row=20,column=1)
        sub5_button = ctk.CTkComboBox(self.scrollable_frame, variable=sub5, values=all_players, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub5_button.grid(row=20,column=2,pady=(4,0)); sub5.set(last_player[14])
        
        # ================= TACTICS ================= #
        tactics = pd.read_excel(open(file2,"rb"), sheet_name="tactics")
        tix = tactics.Tactics.tolist()
        #tactic variables
        tac1=StringVar();tac2=StringVar();tac3=StringVar();tac4=StringVar();tac5=StringVar();tac6=StringVar();mstr=StringVar()
        deff_tacs = ["DD","MM","GIH","ZD","POD","OST"]
        mid_tacs = ["PP","KP","AOB","PTW","FM","SD"]
        att_tacs = ["SOS","CS","RAD","LP","AB","DFF"]
        master_tac = [""] + deff_tacs + mid_tacs + att_tacs
        #tac_btn1
        tac_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Def Tac 1');  tac_txt1.grid(row=6,column=5)
        tac_btn1 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac1, values=deff_tacs, width=75); tac1.set(tix[0]); tac_btn1.grid(row=6,column=6)
        #tac_btn2
        tac_txt2 = ctk.CTkLabel(self.scrollable_frame,text ='Def Tac 2'); tac_txt2.grid(row=7,column=5)
        tac_btn2 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac2, values=deff_tacs, width=75); tac2.set(tix[1]); tac_btn2.grid(row=7,column=6)
                #tac_btn2
        tac_txt3 = ctk.CTkLabel(self.scrollable_frame,text ='Mid Tac 1'); tac_txt3.grid(row=8,column=5)
        tac_btn3 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac3, values=mid_tacs, width=75); tac3.set(tix[2]); tac_btn3.grid(row=8,column=6)
                #tac_btn2
        tac_txt4 = ctk.CTkLabel(self.scrollable_frame,text ='Mid Tac 2'); tac_txt4.grid(row=9,column=5)
        tac_btn4 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac4, values=mid_tacs, width=75); tac4.set(tix[3]); tac_btn4.grid(row=9,column=6)
                #tac_btn2
        tac_txt5 = ctk.CTkLabel(self.scrollable_frame,text ='Att Tac 1'); tac_txt5.grid(row=10,column=5)
        tac_btn5 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac5, values=att_tacs, width=75); tac5.set(tix[4]); tac_btn5.grid(row=10,column=6)
                #tac_btn2
        tac_txt6 = ctk.CTkLabel(self.scrollable_frame,text ='Att Tac 2'); tac_txt6.grid(row=11,column=5)
        tac_btn6 = ctk.CTkOptionMenu(self.scrollable_frame, variable=tac6, values=att_tacs, width=75); tac6.set(tix[5]); tac_btn6.grid(row=11,column=6)
                #tac_btn2
        mstr_txt = ctk.CTkLabel(self.scrollable_frame,text ='Master'); mstr_txt.grid(row=12,column=5)
        mstr_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=mstr, values=master_tac, width=75); mstr.set(tix[6]); mstr_btn.grid(row=12,column=6)

        # ================= ROLES ================= #
        cpt=StringVar();frk=StringVar();pen=StringVar()
        roles_prev = pd.read_excel(open(file2,"rb"), sheet_name="roles")
        roles_prev.drop(list(roles_prev.filter(regex='Unna')), axis=1, inplace=True)
        rr = roles_prev.Role.tolist()
        if len(rr) < 1:
            rr = ("Choose","Choose","Choose")
        else:
            pass
                
        cpt_txt = ctk.CTkLabel(self.scrollable_frame,text ='Captain'); cpt_txt.grid(row=14,column=5)
        cpt_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=cpt, values=roles_list, width=100); cpt.set(rr[0]); cpt_btn.grid(row=14,column=6)
        
        frk_txt = ctk.CTkLabel(self.scrollable_frame,text ='Freekicks'); frk_txt.grid(row=15,column=5)
        frk_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=frk, values=roles_list, width=100); frk.set(rr[1]); frk_btn.grid(row=15,column=6)
        
        pen_txt = ctk.CTkLabel(self.scrollable_frame,text ='Penalties'); pen_txt.grid(row=16,column=5)
        pen_btn = ctk.CTkOptionMenu(self.scrollable_frame, variable=pen, values=roles_list, width=100); pen.set(rr[2]); pen_btn.grid(row=16,column=6) 


        # ================= SUBSTITUTES =============== #
        prev_subs = pd.read_excel(open(file2,"rb"), sheet_name="subs")
        prev_subs.drop(list(prev_subs.filter(regex='Unna')), axis=1, inplace=True)
        prev_subs = prev_subs.fillna("")
        prev_circ = prev_subs.Circumstance.tolist()
        prev_on = prev_subs["Player On"].tolist()
        prev_off = prev_subs["Player Off"].tolist()
        prev_pos = prev_subs.Position.tolist()
        
        # Initialize an empty list to store the variables
        mins = []
        
        # Iterate over the 'Minute' column in prev_subs and convert to integers
        for item in prev_subs['Minute']:
            if isinstance(item, (int, float)):  # Check if it's a numeric value
                mins.append(int(item))  # Convert to int if it's numeric
            else:
                mins.append("")  # Append empty string if not numeric
        
        sub1_min=StringVar();sub2_min=StringVar();sub3_min=StringVar();sub4_min=StringVar();sub5_min=StringVar();
        sub1_circ=StringVar();sub2_circ=StringVar();sub3_circ=StringVar();sub4_circ=StringVar();sub5_circ=StringVar();
        sub1_on=StringVar();sub2_on=StringVar();sub3_on=StringVar();sub4_on=StringVar();sub5_on=StringVar();
        sub1_off=StringVar();sub2_off=StringVar();sub3_off=StringVar();sub4_off=StringVar();sub5_off=StringVar();
        sub1_pos=StringVar();sub2_pos=StringVar();sub3_pos=StringVar();sub4_pos=StringVar();sub5_pos=StringVar();

        circumstances = ["","Any","Winning","Drawing","Losing", "Not Winning", "Not Losing", "Not Drawing"]
        
        #row 22 for 7 rows + 1 row for space
        sub_opt_txt = ctk.CTkLabel(self.scrollable_frame,text ='Sub Options',text_color="white", font=("Helvetica",14)); sub_opt_txt.grid(row=22,column=1, pady=10)

        sub_id_txt = ctk.CTkLabel(self.scrollable_frame,text ='Minute',text_color="white", font=("Helvetica",12)); sub_id_txt.grid(row=23,column=1, pady=5)
        sub_con_txt = ctk.CTkLabel(self.scrollable_frame,text ='Circumstance',text_color="white", font=("Helvetica",12)); sub_con_txt.grid(row=23,column=2, pady=5)
        sub_on_txt = ctk.CTkLabel(self.scrollable_frame,text ='Player On',text_color="white", font=("Helvetica",12)); sub_on_txt.grid(row=23,column=3, pady=5)
        sub_off_txt = ctk.CTkLabel(self.scrollable_frame,text ='Player Off',text_color="white", font=("Helvetica",12)); sub_off_txt.grid(row=23,column=4, pady=5)
        sub_pos_txt = ctk.CTkLabel(self.scrollable_frame,text ='Position',text_color="white", font=("Helvetica",12)); sub_pos_txt.grid(row=23,column=5, pady=5)

        
        sub1_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub1_min, width=60);  sub1_min.set(str(mins[0])); sub1_time.grid(row=24,column=1,padx=2,pady=2)
        sub1_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub1_circ, values=circumstances, width=120); sub1_con.set(prev_circ[0]); sub1_con.grid(row=24,column=2,padx=2,pady=2)
        sub1_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub1_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub1_pl_on.set(prev_on[0]); sub1_pl_on.grid(row=24,column=3,padx=2,pady=2)
        sub1_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub1_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub1_pl_off.set(prev_off[0]);  sub1_pl_off.grid(row=24,column=4,padx=2,pady=2)
        sub1_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub1_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub1_role.set(prev_pos[0]);  sub1_role.grid(row=24,column=5,padx=2,pady=2)
        
        sub2_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub2_min, width=60);  sub2_min.set(mins[1]); sub2_time.grid(row=25,column=1,padx=2,pady=2)
        sub2_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub2_circ, values=circumstances, width=120); sub2_con.set(prev_circ[1]); sub2_con.grid(row=25,column=2,padx=2,pady=2)
        sub2_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub2_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub2_pl_on.set(prev_on[1]); sub2_pl_on.grid(row=25,column=3,padx=2,pady=2)
        sub2_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub2_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub2_pl_off.set(prev_off[1]);  sub2_pl_off.grid(row=25,column=4,padx=2,pady=2)
        sub2_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub2_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283");  sub2_role.set(prev_pos[1]); sub2_role.grid(row=25,column=5,padx=2,pady=2)
        
        sub3_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub3_min, width=60); sub3_min.set(mins[2]); sub3_time.grid(row=26,column=1,padx=2,pady=2)
        sub3_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub3_circ, values=circumstances, width=120); sub3_con.set(prev_circ[2]); sub3_con.grid(row=26,column=2,padx=2,pady=2)
        sub3_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub3_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub3_pl_on.set(prev_on[2]); sub3_pl_on.grid(row=26,column=3,padx=2,pady=2)
        sub3_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub3_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub3_pl_off.set(prev_off[2]);  sub3_pl_off.grid(row=26,column=4,padx=2,pady=2)
        sub3_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub3_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub3_role.set(prev_pos[2]);  sub3_role.grid(row=26,column=5,padx=2,pady=2)
        
        sub4_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub4_min, width=60); sub4_min.set(mins[3]);  sub4_time.grid(row=27,column=1,padx=2,pady=2)
        sub4_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub4_circ, values=circumstances, width=120); sub4_con.set(prev_circ[3]); sub4_con.grid(row=27,column=2,padx=2,pady=2)
        sub4_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub4_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974");  sub4_pl_on.set(prev_on[3]); sub4_pl_on.grid(row=27,column=3,padx=2,pady=2)
        sub4_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub4_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub4_pl_off.set(prev_off[3]);  sub4_pl_off.grid(row=27,column=4,padx=2,pady=2)
        sub4_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub4_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub4_role.set(prev_pos[3]);   sub4_role.grid(row=27,column=5,padx=2,pady=2)

        sub5_time = ctk.CTkEntry(self.scrollable_frame, textvariable=sub5_min, width=60); sub5_min.set(mins[4]);  sub5_time.grid(row=28,column=1,padx=2,pady=2)
        sub5_con = ctk.CTkOptionMenu(self.scrollable_frame, variable=sub5_circ, values=circumstances, width=120); sub5_con.set(prev_circ[4]); sub5_con.grid(row=28,column=2,padx=2,pady=2)
        sub5_pl_on = ctk.CTkComboBox(self.scrollable_frame, variable=sub5_on, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub5_pl_on.set(prev_on[4]);  sub5_pl_on.grid(row=28,column=3,padx=2,pady=2)
        sub5_pl_off = ctk.CTkComboBox(self.scrollable_frame, variable=sub5_off, values=roles_list, fg_color="#0b474a", button_hover_color="#339a8d", border_color="#0b6974", button_color="#0b6974"); sub5_pl_off.set(prev_off[4]);  sub5_pl_off.grid(row=28,column=4,padx=2,pady=2)
        sub5_role = ctk.CTkComboBox(self.scrollable_frame, variable=sub5_pos, values=all_pos, width=70, fg_color="#471f5f", border_color="#6a6283",button_color="#6a6283"); sub5_role.set(prev_pos[4]);  sub5_role.grid(row=28,column=5,padx=2,pady=2)
        

        # ================= ACTIONS ================= #
        name1=StringVar();name2=StringVar();name3=StringVar();name4=StringVar();name5=StringVar()
        action1=StringVar();action2=StringVar();action3=StringVar();action4=StringVar();action5=StringVar()
        roles_list.insert(0,"")
        # get last week's submitted actions
        actions_prev = pd.read_excel(open(file2,"rb"), sheet_name="actions")
        np = actions_prev.Player.fillna("").tolist()
        ap = actions_prev.Action.fillna("").tolist()

        action_txt = ctk.CTkLabel(self.scrollable_frame,text ='Actions',text_color="white", font=("Helvetica",14)); action_txt.grid(row=30,column=1, pady=10)
        
        #action btn 1
        act_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Name');  act_txt1.grid(row=31,column=1, padx=5,pady=(4,0))
        act_btn1 = ctk.CTkComboBox(self.scrollable_frame, variable=name1, values=roles_list); act_btn1.grid(row=31,column=2); name1.set(np[0]);
        lst_txt1 = ctk.CTkLabel(self.scrollable_frame,text ='Action');  lst_txt1.grid(row=31,column=3,padx=2.5)
        list1 = ctk.CTkComboBox(self.scrollable_frame, variable=action1); action1.set(ap[0]); list1.grid(row=31,column=4);
        
        #action btn 2
        act_btn2 = ctk.CTkComboBox(self.scrollable_frame, variable=name2, values=roles_list); act_btn2.grid(row=32,column=2); name2.set(np[1]);
        list2 = ctk.CTkComboBox(self.scrollable_frame, variable=action2); action2.set(ap[1]); list2.grid(row=32,column=4);

        #action btn 3
        act_btn3 = ctk.CTkComboBox(self.scrollable_frame, variable=name3, values=roles_list); act_btn3.grid(row=33,column=2); name3.set(np[2]);
        list3 = ctk.CTkComboBox(self.scrollable_frame, variable=action3); action3.set(ap[2]); list3.grid(row=33,column=4);

        #action btn 4
        act_btn4 = ctk.CTkComboBox(self.scrollable_frame, variable=name4, values=roles_list); act_btn4.grid(row=34,column=2); name4.set(np[3]);
        list4 = ctk.CTkComboBox(self.scrollable_frame, variable=action4); action4.set(ap[3]); list4.grid(row=34,column=4);

        #action btn 5
        act_btn5 = ctk.CTkComboBox(self.scrollable_frame, variable=name5,  values=roles_list); act_btn5.grid(row=35,column=2); name5.set(np[4]);
        list5 = ctk.CTkComboBox(self.scrollable_frame, variable=action5); action5.set(ap[4]); list5.grid(row=35,column=4); 
 
        CTkScrollableDropdown(list1, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action1.set(e),list1.set(e)))
        CTkScrollableDropdown(list2, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action2.set(e),list2.set(e)))
        CTkScrollableDropdown(list3, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action3.set(e),list3.set(e)))
        CTkScrollableDropdown(list4, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action4.set(e),list4.set(e)))
        CTkScrollableDropdown(list5, values=actions_list, justify="left", button_color="transparent", height=400, autocomplete=True, command=lambda e: (action5.set(e),list5.set(e)))

        list1.set(ap[0])
        list2.set(ap[1])
        list3.set(ap[2])
        list4.set(ap[3])
        list5.set(ap[4])        
     

        
        # ================= PASSWORD ================= #
        passwd = StringVar()
        passwd_txt = ctk.CTkLabel(self.scrollable_frame,text ='Password')
        passwd_txt.grid(row=21,column=7)
        passwd_input = passwd_input = ctk.CTkEntry(self.scrollable_frame, textvariable=passwd)
        passwd_input.grid(row=21,column=8,columnspan=4)

        
        # ================= FORMATIONS ================= #
        Formation_txt =  ctk.CTkLabel(self.scrollable_frame,text="Formation: ",font=("Helvetica",16)).grid(row=2, column=6, padx=(10,0))
        global formation
        formation = pd.read_excel(open(file2,"rb"), sheet_name="formations")
        formation.drop(list(formation.filter(regex='Unna')), axis=1, inplace=True)
        formation = formation.squeeze()
        
        def five_four_one(self):
            global formation; formation = 541

            # Update PL5 with Deff names
            PL5_button.configure(values=Deff_names)
            PL5_pos.configure(values=deff_pos)
            
             # Update PL6 to Deff
            PL6_button.configure(values=Deff_names)
            PL6_pos.configure(values=deff_pos)

            # Update PL8 with Mid_names
            PL8_button.configure(values=Mid_names)
            PL8_pos.configure(values=mid_pos)
            
            # Update PL9 with Mid
            PL9_button.configure(values=Mid_names)
            PL9_pos.configure(values=mid_pos)
            
            # Update PL10 to Att
            PL10_button.configure(values=Mid_names)
            PL10_pos.configure(values=mid_pos)

            P5_txt.configure(text="Defender 4") # Update label
            P6_txt.configure(text="Defender 5")
            P7_txt.configure(text="Midfielder 1")
            P8_txt.configure(text="Midfielder 2")
            P9_txt.configure(text="Midfielder 3")
            P10_txt.configure(text="Midfielder 4")
            P11_txt.configure(text="Attacker 1")
            
            form_541.configure(state="disabled") # Disable the button
            form_532.configure(state="normal") # Disable the button
            form_442.configure(state="normal") # Disable the button
            form_451.configure(state="normal") # Disable the button
            form_433.configure(state="normal")
            form_343.configure(state="normal")
            form_334.configure(state="normal")
            
        # 541 button
        form_541 = ctk.CTkButton(self.scrollable_frame, text="541", width=75,  fg_color="#1f8c9c", hover_color="#547588", command=lambda: five_four_one(self))
        form_541.grid(row=2, column=7)

        def five_three_two(self):
            global formation; formation = 532

            # Update PL5 with Deff names
            PL5_button.configure(values=Deff_names)
            PL5_pos.configure(values=deff_pos)
            
             # Update PL6 to Deff
            PL6_button.configure(values=Deff_names)
            PL6_pos.configure(values=deff_pos)

            # Update PL8 with Mid_names
            PL8_button.configure(values=Mid_names)
            PL8_pos.configure(values=mid_pos)
            
            # Update PL9 with Mid
            PL9_button.configure(values=Mid_names)
            PL9_pos.configure(values=mid_pos)
            
            # Update PL10 to Att
            PL10_button.configure(values=Att_names)
            PL10_pos.configure(values=att_pos)

            P5_txt.configure(text="Defender 4") # Update label
            P6_txt.configure(text="Defender 5") # Update label
            P7_txt.configure(text="Midfielder 1")
            P8_txt.configure(text="Midfielder 2")
            P9_txt.configure(text="Midfielder 3")               
            P10_txt.configure(text="Attacker 1")
            P11_txt.configure(text="Attacker 2")

            form_541.configure(state="normal") # Disable the button
            form_532.configure(state="disabled") # Disable the button
            form_442.configure(state="normal") # Disable the button
            form_451.configure(state="normal") # Disable the button
            form_433.configure(state="normal")
            form_343.configure(state="normal")
            form_334.configure(state="normal")
            
        # 532 button
        form_532 = ctk.CTkButton(self.scrollable_frame, text="532",  width=75,  fg_color="#1f8c9c", hover_color="#547588", command=lambda: five_three_two(self))
        form_532.grid(row=2, column=8)

        def four_four_two(self):
            global formation; formation = 442

            # Update PL5 with Deff names
            PL5_button.configure(values=Deff_names)
            PL5_pos.configure(values=deff_pos)
            
             # Update PL6 to Mid
            PL6_button.configure(values=Mid_names)
            PL6_pos.configure(values=mid_pos)

            # Update PL8 with Mid_names
            PL8_button.configure(values=Mid_names)
            PL8_pos.configure(values=mid_pos)
            
            # Update PL9 with Mid
            PL9_button.configure(values=Mid_names)
            PL9_pos.configure(values=mid_pos)
            
            # Update PL10 to Att
            PL10_button.configure(values=Att_names)
            PL10_pos.configure(values=att_pos)

            P5_txt.configure(text="Defender 4") # Update label
            P6_txt.configure(text="Midfielder 1") # Update label
            P7_txt.configure(text="Midfielder 2")
            P8_txt.configure(text="Midfielder 3")
            P9_txt.configure(text="Midfielder 4")               
            P10_txt.configure(text="Attacker 1")
            P11_txt.configure(text="Attacker 2")
            
            form_541.configure(state="normal") # Disable the button
            form_532.configure(state="normal") # Disable the button
            form_442.configure(state="disabled") # Disable the button
            form_451.configure(state="normal") # Disable the button
            form_433.configure(state="normal")
            form_343.configure(state="normal")
            form_334.configure(state="normal")
            
        # 442 button
        form_442 = ctk.CTkButton(self.scrollable_frame, text="442",  width=75,  fg_color="#1f8c9c", hover_color="#547588", command=lambda: four_four_two(self))
        form_442.grid(row=2, column=9)

        def four_five_one(self):
            global formation
            formation = 451
            print(formation)

            # Update PL5 with Mid_names
            PL5_button.configure(values=Deff_names)
            PL5_pos.configure(values=deff_pos)
            
            # Update PL6 with Mid_names
            PL6_button.configure(values=Mid_names)
            PL6_pos.configure(values=mid_pos)

            # Update PL8 with Mid_names
            PL8_button.configure(values=Mid_names)
            PL8_pos.configure(values=mid_pos)
            
            # Update PL9 with Mid
            PL9_button.configure(values=Mid_names)
            PL9_pos.configure(values=mid_pos)
            
            # Update PL10 with Mid_names
            PL10_button.configure(values=Mid_names)
            PL10_pos.configure(values=mid_pos)
            
            # Update labels
            P5_txt.configure(text="Defender 4") # Update label
            P6_txt.configure(text="Midfielder 1")
            P7_txt.configure(text="Midfielder 2")
            P8_txt.configure(text="Midfielder 3")
            P9_txt.configure(text="Midfielder 4")
            P10_txt.configure(text="Midfielder 5")
            P11_txt.configure(text="Attacker 1")
        
            # Disable/Enable buttons
            form_541.configure(state="normal")
            form_532.configure(state="normal")
            form_442.configure(state="normal")
            form_451.configure(state="disabled")
            form_433.configure(state="normal")
            form_343.configure(state="normal")
            form_334.configure(state="normal")
            
        # 451 button
        form_451 = ctk.CTkButton(self.scrollable_frame, text="451",  width=75,  fg_color="#1f8c9c", hover_color="#547588", command=lambda: four_five_one(self))
        form_451.grid(row=2, column=10, padx=(2,0))


        def four_three_three(self):
            global formation
            formation = 433
            print(formation)

            # Update PL5 with Deff names
            PL5_button.configure(values=Deff_names)
            PL5_pos.configure(values=deff_pos)
            
            # Update PL6 with Mid_names
            PL6_button.configure(values=Mid_names)
            PL6_pos.configure(values=mid_pos)

            # Update PL8 with Mid_names
            PL8_button.configure(values=Mid_names)
            PL8_pos.configure(values=mid_pos)
            
            # Update PL9 with Att
            PL9_button.configure(values=Att_names)
            PL9_pos.configure(values=att_pos)
            
            # Update PL10 with Att
            PL10_button.configure(values=Att_names)
            PL10_pos.configure(values=att_pos)
            
            # Update labels
            P5_txt.configure(text="Defender 4") # Update label
            P6_txt.configure(text="Midfielder 1")
            P7_txt.configure(text="Midfielder 2")
            P8_txt.configure(text="Midfielder 3")
            P9_txt.configure(text="Attacker 1")
            P10_txt.configure(text="Attacker 2")
            P11_txt.configure(text="Attacker 3")
        
            # Disable/Enable buttons
            form_541.configure(state="normal")
            form_532.configure(state="normal")
            form_442.configure(state="normal")
            form_451.configure(state="normal")
            form_433.configure(state="disabled")
            form_343.configure(state="normal")
            form_334.configure(state="normal")
        
        # 442 button
        form_433 = ctk.CTkButton(self.scrollable_frame, text="433",  width=75,  fg_color="#1f8c9c", hover_color="#547588", command=lambda: four_three_three(self))
        form_433.grid(row=2, column=11, padx=(2,0))

        def three_four_three(self):
            global formation
            formation = 343
            print(formation)

            # Update PL5 with Mid_names
            PL5_button.configure(values=Mid_names)
            PL5_pos.configure(values=mid_pos)
            
            # Update PL6 with Mid_names
            PL6_button.configure(values=Mid_names)
            PL6_pos.configure(values=mid_pos)

            # Update PL8 with Mid_names
            PL8_button.configure(values=Mid_names)
            PL8_pos.configure(values=mid_pos)
            
            # Update PL9 with Att
            PL9_button.configure(values=Att_names)
            PL9_pos.configure(values=att_pos)
            
            # Update PL10 with Att
            PL10_button.configure(values=Att_names)
            PL10_pos.configure(values=att_pos)
            
            # Update labels
            P5_txt.configure(text="Midfielder 1")
            P6_txt.configure(text="Midfielder 2")
            P7_txt.configure(text="Midfielder 3")
            P8_txt.configure(text="Midfielder 4")
            P9_txt.configure(text="Attacker 1")
            P10_txt.configure(text="Attacker 2")
            P11_txt.configure(text="Attacker 3")
        
            # Disable/Enable buttons
            form_541.configure(state="normal")
            form_532.configure(state="normal")
            form_442.configure(state="normal")
            form_451.configure(state="normal")
            form_433.configure(state="normal")
            form_343.configure(state="disabled")
            form_334.configure(state="normal")

                # 442 button
        form_343 = ctk.CTkButton(self.scrollable_frame, text="343",  width=75,  fg_color="#1f8c9c", hover_color="#547588", command=lambda: three_four_three(self))
        form_343.grid(row=2, column=12, padx=(2,0))

        def three_three_four(self):
            global formation
            formation = 334
            print(formation)

            # Update PL5 with Mid_names
            PL5_button.configure(values=Mid_names)
            PL5_pos.configure(values=mid_pos)
            
            # Update PL6 with Mid_names
            PL6_button.configure(values=Mid_names)
            PL6_pos.configure(values=mid_pos)

            # Update PL8 with Mid_names
            PL8_button.configure(values=Att_names)
            PL8_pos.configure(values=att_pos)
            
            # Update PL9 with Att
            PL9_button.configure(values=Att_names)
            PL9_pos.configure(values=att_pos)
            
            # Update PL10 with Att
            PL10_button.configure(values=Att_names)
            PL10_pos.configure(values=att_pos)
            
            # Update labels
            P5_txt.configure(text="Midfielder 1")
            P6_txt.configure(text="Midfielder 2")
            P7_txt.configure(text="Midfielder 3")
            P8_txt.configure(text="Attacker 1")
            P9_txt.configure(text="Attacker 2")
            P10_txt.configure(text="Attacker 3")
            P11_txt.configure(text="Attacker 4")
        
            # Disable/Enable buttons
            form_541.configure(state="normal")
            form_532.configure(state="normal")
            form_442.configure(state="normal")
            form_451.configure(state="normal")
            form_433.configure(state="normal")
            form_343.configure(state="normal")
            form_334.configure(state="disabled")

                # 442 button
        form_334 = ctk.CTkButton(self.scrollable_frame, text="334",  width=75,  fg_color="#1f8c9c", hover_color="#547588", command=lambda: three_three_four(self))
        form_334.grid(row=2, column=13, padx=(2,0))

        if formation == 442:
            four_four_two(self)
        elif formation == 532:
            five_three_two(self)
        elif formation == 541:
            five_four_one(self)
        elif formation == 451:
            four_five_one(self)
        else:
            pass
            
        sub5.set(last_player[14])

        # ============================================ #
        # ================= GET INFO ================= #
        # ============================================ #
        def set_youth_team(self):
            # make tuple of players and positions to pass to the submit function
            self.players = (PL1.get(), PL2.get(), PL3.get(), PL4.get(), PL5.get(), PL6.get(), PL7.get(), PL8.get(), PL9.get(), PL10.get(), PL11.get(), sub1.get(), sub2.get(), sub3.get(), sub4.get(), sub5.get())
            self.positions = (Pos2.get(), Pos3.get(), Pos4.get(), Pos5.get(), Pos6.get(), Pos7.get(), Pos8.get(), Pos9.get(), Pos10.get(), Pos11.get(), "sub1", "sub2", "sub3", "sub4", "sub5")
            self.tactics = (tac1.get(),tac2.get(),tac3.get(),tac4.get(),tac5.get(),tac6.get(),mstr.get())
            self.roles = (cpt.get(),frk.get(),pen.get())
            self.roles_df = roles_df
            self.names = (name1.get(),name2.get(),name3.get(),name4.get(),name5.get())
            self.actions = (action1.get(),action2.get(),action3.get(),action4.get(),action5.get())
            self.password = passwd.get()
            self.substitute_options = {
                "Minute": [sub1_min.get(),sub2_min.get(),sub3_min.get(),sub4_min.get(),sub5_min.get()],
                "Circumstance" : [sub1_circ.get(),sub2_circ.get(),sub3_circ.get(),sub4_circ.get(),sub5_circ.get()],
                "Player On" : [sub1_on.get(),sub2_on.get(),sub3_on.get(),sub4_on.get(),sub5_on.get()],
                "Player Off" : [sub1_off.get(),sub2_off.get(),sub3_off.get(),sub4_off.get(),sub5_off.get()],
                "Position" : [sub1_pos.get(),sub2_pos.get(),sub3_pos.get(),sub4_pos.get(),sub5_pos.get()]
            }
            self.subs = pd.DataFrame(self.substitute_options)
            self.submit_button.configure(state="normal")
            
            print(f"{self.players},\n{self.positions,self.tactics,self.roles} \nNames: {self.names} \nActions: {self.actions} \nFormation = {formation}")
            print(f'Password entered is "{self.password}"')
            

            
        
        # set button
        set_btn = ctk.CTkButton(self.scrollable_frame, text="Set Youth Team", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: set_youth_team(self)) # set button
        set_btn.grid(row=1, column=4,pady=10, padx=10)

        # ================= SUBMIT ================= #
        self.submit_button = ctk.CTkButton(self.scrollable_frame, text="Submit", width=100, fg_color="#0b6974", hover_color="#547588", command=lambda: self.controller.submit_yth_team(self.players,self.positions,
                                                                                                                                                                                       self.tactics,self.roles,self.roles_df,self.actions,
                                                                                                                                                                                       self.names,self.password,formation,self.subs))
        self.submit_button.configure(state=DISABLED)
        self.submit_button.grid(row=1, column=3,pady=10, padx=10)


# ## Execute

# In[6]:


if __name__ == "__main__":
    app = UEApp()
    app.mainloop()


# In[ ]:




