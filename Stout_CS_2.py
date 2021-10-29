{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import math\n",
    "import hashlib\n",
    "import numpy as np\n",
    "\n",
    "# Read in CSV file with proper Headers\n",
    "orders = pd.read_csv('casestudy.csv')\n",
    "orders.columns = [\"index\", \"CUSTOMER_EMAIL\", \"Net Revenue\", \"Year\"]\n",
    "\n",
    "# Drop duplicate index column\n",
    "orders = orders.drop(['index'], axis = 1)\n",
    "\n",
    "# Create unique hash identifiers for each customer email\n",
    "orders['CUSTOMER_EMAIL'] = orders['CUSTOMER_EMAIL'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())\n",
    "\n",
    "orders.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "CUSTOMER_EMAIL    249987\n",
       "Net Revenue       249987\n",
       "Year              249987\n",
       "dtype: int64"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Now that we have a dataframe containing index, email (encoded), net revenue, and year, we can move on\n",
    "#  We will begin by creating segmented dataframes for each year, so 3 new dataframes\n",
    "\n",
    "orders2017 = orders.loc[orders['Year'] == 2017]\n",
    "orders2016 = orders.loc[orders['Year'] == 2016]\n",
    "orders2015 = orders.loc[orders['Year'] == 2015]\n",
    "\n",
    "\n",
    "#  Although unnamed, it should be okay that I dropped the duplicate 'index' column because the values are unchanged even after being segmented\n",
    "orders2017.count()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2015</th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Total Revenue</th>\n",
       "      <td>29036749.19</td>\n",
       "      <td>25730943.59</td>\n",
       "      <td>31417495.03</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                      2015         2016         2017\n",
       "Total Revenue  29036749.19  25730943.59  31417495.03"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#######   Metrics are for each year   #######\n",
    "\n",
    "## Total Revenue for the Current Year\n",
    "total_rev2015 = orders2015['Net Revenue'].sum()\n",
    "total_rev2016 = orders2016['Net Revenue'].sum()\n",
    "total_rev2017 = orders2017['Net Revenue'].sum()\n",
    "\n",
    "total_rev = pd.DataFrame({'2015': [total_rev2015],\n",
    "                   '2016': [total_rev2016],\n",
    "                   '2017': [total_rev2017]},\n",
    "                  index=['Total Revenue'])\n",
    "#total_rev = pd.DataFrame([total_rev2015, total_rev2016, total_rev2015])\n",
    "#total_rev.columns = ['Total Revenue']\n",
    "\n",
    "total_rev\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 91,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2015</th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>New Customer Revenue</th>\n",
       "      <td>0</td>\n",
       "      <td>18245491.01</td>\n",
       "      <td>28776235.04</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                      2015         2016         2017\n",
       "New Customer Revenue     0  18245491.01  28776235.04"
      ]
     },
     "execution_count": 91,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#  New Customer Revenue e.g., new customers not present in previous year only\n",
    "\n",
    "new_customer_orders2016 = orders2016\n",
    "new_customer_orders2017 = orders2017\n",
    "emails2015 = orders2015['CUSTOMER_EMAIL']\n",
    "emails2016 = orders2016['CUSTOMER_EMAIL']\n",
    "emails2017 = orders2017['CUSTOMER_EMAIL']\n",
    "new_list2016 = list(set(emails2016) - set(emails2015))\n",
    "new_list2017 = list(set(emails2017) - set(emails2016))\n",
    "\n",
    "new_customer_orders2016 = new_customer_orders2016[(emails2016.isin(new_list2016) == True)]\n",
    "new_customer_orders2017 = new_customer_orders2017[(emails2017.isin(new_list2017) == True)]\n",
    "new_rev2016 = new_customer_orders2016['Net Revenue'].sum()\n",
    "new_rev2017 = new_customer_orders2017['Net Revenue'].sum()\n",
    "\n",
    "new_rev = pd.DataFrame({'2015': [0],\n",
    "                   '2016': [new_rev2016],\n",
    "                   '2017': [new_rev2017]},\n",
    "                  index=['New Customer Revenue'])\n",
    "#total_rev = pd.DataFrame([total_rev2015, total_rev2016, total_rev2015])\n",
    "#total_rev.columns = ['Total Revenue']\n",
    "\n",
    "new_rev"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 68,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Existing Customer Growth</th>\n",
       "      <td>0.272406</td>\n",
       "      <td>120.581361</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                              2016        2017\n",
       "Existing Customer Growth  0.272406  120.581361"
      ]
     },
     "execution_count": 68,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#  Existing Customer Growth\n",
    "existing_list2016 = list(set(emails2016) - (set(emails2016) - set(emails2015)))\n",
    "ex_customer_orders2016 = orders2016[(emails2016.isin(existing_list2016) == True)]\n",
    "ex_helper2015 = orders2015[(emails2015.isin(existing_list2016) == True)]\n",
    "ex_cust_growth2016 = ((ex_customer_orders2016['Net Revenue'].sum() - ex_helper2015['Net Revenue'].sum()) / ex_helper2015['Net Revenue'].sum()) * 100\n",
    "ex_cust_growth2016  \n",
    "\n",
    "existing_list2017 = list(set(emails2017) - (set(emails2017) - set(emails2016)))\n",
    "ex_customer_orders2017 = orders2017[(emails2017.isin(existing_list2017) == True)]\n",
    "ex_helper2016 = orders2016[(emails2016.isin(existing_list2017) == True)]\n",
    "ex_helper2015_2 = orders2015[(emails2015.isin(existing_list2017) == True)]   # To account for existing customers from both years\n",
    "\n",
    "ex_cust_growth2017 = ((ex_customer_orders2016['Net Revenue'].sum() - ex_helper2015_2['Net Revenue'].sum() \n",
    "                    - ex_helper2016['Net Revenue'].sum()) / (ex_helper2015_2['Net Revenue'].sum()+ ex_helper2016['Net Revenue'].sum())) * 100\n",
    "ex_cust_growth2017\n",
    "\n",
    "\n",
    "ex_growth = pd.DataFrame({'2016': [ex_cust_growth2016],\n",
    "                   '2017': [ex_cust_growth2017],\n",
    "                   },\n",
    "                  index=['Existing Customer Growth'])\n",
    "ex_growth"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 71,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Attrition</th>\n",
       "      <td>0.113849</td>\n",
       "      <td>-0.221001</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "               2016      2017\n",
       "Attrition  0.113849 -0.221001"
      ]
     },
     "execution_count": 71,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Revenue Lost from Attrition\n",
    "# The formula I used for this is: (prev year rev - current year rev) / prev year rev\n",
    "attrition2016 = (orders2015['Net Revenue'].sum() - orders2016['Net Revenue'].sum()) / orders2015['Net Revenue'].sum()\n",
    "attrition2017 = (orders2016['Net Revenue'].sum() - orders2017['Net Revenue'].sum()) / orders2016['Net Revenue'].sum()\n",
    "\n",
    "attrition = pd.DataFrame({'2016': [attrition2016],\n",
    "                   '2017': [attrition2017],\n",
    "                   },\n",
    "                  index=['Attrition'])\n",
    "attrition"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 72,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Existing Customer Revenue (Current Year)</th>\n",
       "      <td>7485452.58</td>\n",
       "      <td>2641259.99</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                2016        2017\n",
       "Existing Customer Revenue (Current Year)  7485452.58  2641259.99"
      ]
     },
     "execution_count": 72,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Existing Customer Revenue Current Year\n",
    "ex_cust_rev2016 = ex_customer_orders2016['Net Revenue'].sum()\n",
    "ex_cust_rev2017 = ex_customer_orders2017['Net Revenue'].sum()\n",
    "\n",
    "ex_cust_rev = pd.DataFrame({'2016': [ex_cust_rev2016],\n",
    "                   '2017': [ex_cust_rev2017],\n",
    "                   },\n",
    "                  index=['Existing Customer Revenue (Current Year)'])\n",
    "ex_cust_rev"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 74,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Existing Customer Revenue (Prior Year)</th>\n",
       "      <td>7465117.12</td>\n",
       "      <td>2620648.65</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                              2016        2017\n",
       "Existing Customer Revenue (Prior Year)  7465117.12  2620648.65"
      ]
     },
     "execution_count": 74,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Existing Customer Revenue Prior Year\n",
    "ex_cust_rev_prior2016 = ex_helper2015['Net Revenue'].sum()\n",
    "ex_cust_rev_prior2017 = ex_helper2016['Net Revenue'].sum()\n",
    "\n",
    "ex_cust_rev_p = pd.DataFrame({'2016': [ex_cust_rev_prior2016],\n",
    "                   '2017': [ex_cust_rev_prior2017],\n",
    "                   },\n",
    "                  index=['Existing Customer Revenue (Prior Year)'])\n",
    "ex_cust_rev_p"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 82,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2015</th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Total Customers Current Year</th>\n",
       "      <td>231294</td>\n",
       "      <td>204646</td>\n",
       "      <td>249987</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                2015    2016    2017\n",
       "Total Customers Current Year  231294  204646  249987"
      ]
     },
     "execution_count": 82,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "###  Total Customers Current Year\n",
    "tot_cust2015 = orders2015['CUSTOMER_EMAIL'].count()\n",
    "tot_cust2016 = orders2016['CUSTOMER_EMAIL'].count()\n",
    "tot_cust2017 = orders2017['CUSTOMER_EMAIL'].count()\n",
    "\n",
    "total_cust = pd.DataFrame({'2015': [tot_cust2015],\n",
    "                   '2016': [tot_cust2016],\n",
    "                   '2017': [tot_cust2017]},\n",
    "                  index=['Total Customers Current Year'])\n",
    "total_cust\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 83,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2015</th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Total Customers Previous Year</th>\n",
       "      <td>0</td>\n",
       "      <td>231294</td>\n",
       "      <td>204646</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                               2015    2016    2017\n",
       "Total Customers Previous Year     0  231294  204646"
      ]
     },
     "execution_count": 83,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "###  Total Customers Previous Year\n",
    "tot_cust2015_prev = 0\n",
    "tot_cust2016_prev = orders2015['CUSTOMER_EMAIL'].count()\n",
    "tot_cust2017_prev = orders2016['CUSTOMER_EMAIL'].count()\n",
    "\n",
    "total_cust_prev = pd.DataFrame({'2015': [tot_cust2015_prev],\n",
    "                   '2016': [tot_cust2016_prev],\n",
    "                   '2017': [tot_cust2017_prev]},\n",
    "                  index=['Total Customers Previous Year'])\n",
    "total_cust_prev\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 86,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2015</th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>New Customers</th>\n",
       "      <td>231294</td>\n",
       "      <td>145062</td>\n",
       "      <td>228262</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                 2015    2016    2017\n",
       "New Customers  231294  145062  228262"
      ]
     },
     "execution_count": 86,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "### New Customers\n",
    "new_cust2015 = orders2015['CUSTOMER_EMAIL'].count()\n",
    "new_cust2016 = len(list(set(emails2016) - set(emails2015)))\n",
    "new_cust2017 = len(list(set(emails2017) - set(emails2016) - set(emails2015)))\n",
    "\n",
    "new_cust = pd.DataFrame({'2015': [new_cust2015],\n",
    "                   '2016': [new_cust2016],\n",
    "                   '2017': [new_cust2017]},\n",
    "                  index=['New Customers'])\n",
    "new_cust\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 89,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>2015</th>\n",
       "      <th>2016</th>\n",
       "      <th>2017</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Lost Customers</th>\n",
       "      <td>231294</td>\n",
       "      <td>171710</td>\n",
       "      <td>354631</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                  2015    2016    2017\n",
       "Lost Customers  231294  171710  354631"
      ]
     },
     "execution_count": 89,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "### Lost Customers\n",
    "lost_cust2015 = orders2015['CUSTOMER_EMAIL'].count()\n",
    "lost_cust2016 = len(list(set(emails2015) - set(emails2016)))\n",
    "lost_cust2017 = len(list(set.union(set(emails2016) - set(emails2017),(set(emails2015) - set(emails2017)))))\n",
    "\n",
    "lost_cust = pd.DataFrame({'2015': [lost_cust2015],\n",
    "                   '2016': [lost_cust2016],\n",
    "                   '2017': [lost_cust2017]},\n",
    "                  index=['Lost Customers'])\n",
    "lost_cust\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 100,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Total Revenue</th>\n",
       "      <th>New Customer Revenue</th>\n",
       "      <th>Existing Customer Growth</th>\n",
       "      <th>Attrition</th>\n",
       "      <th>Existing Customer Revenue (Current Year)</th>\n",
       "      <th>Existing Customer Revenue (Prior Year)</th>\n",
       "      <th>Total Customers Current Year</th>\n",
       "      <th>Total Customers Previous Year</th>\n",
       "      <th>New Customers</th>\n",
       "      <th>Lost Customers</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>2015</th>\n",
       "      <td>29036749.19</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.00</td>\n",
       "      <td>231294.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>231294.0</td>\n",
       "      <td>231294.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2016</th>\n",
       "      <td>25730943.59</td>\n",
       "      <td>18245491.01</td>\n",
       "      <td>0.272406</td>\n",
       "      <td>0.113849</td>\n",
       "      <td>7485452.58</td>\n",
       "      <td>7465117.12</td>\n",
       "      <td>204646.0</td>\n",
       "      <td>231294.0</td>\n",
       "      <td>145062.0</td>\n",
       "      <td>171710.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2017</th>\n",
       "      <td>31417495.03</td>\n",
       "      <td>28776235.04</td>\n",
       "      <td>120.581361</td>\n",
       "      <td>-0.221001</td>\n",
       "      <td>2641259.99</td>\n",
       "      <td>2620648.65</td>\n",
       "      <td>249987.0</td>\n",
       "      <td>204646.0</td>\n",
       "      <td>228262.0</td>\n",
       "      <td>354631.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "      Total Revenue  New Customer Revenue  Existing Customer Growth  \\\n",
       "2015    29036749.19                  0.00                  0.000000   \n",
       "2016    25730943.59           18245491.01                  0.272406   \n",
       "2017    31417495.03           28776235.04                120.581361   \n",
       "\n",
       "      Attrition  Existing Customer Revenue (Current Year)  \\\n",
       "2015   0.000000                                      0.00   \n",
       "2016   0.113849                                7485452.58   \n",
       "2017  -0.221001                                2641259.99   \n",
       "\n",
       "      Existing Customer Revenue (Prior Year)  Total Customers Current Year  \\\n",
       "2015                                    0.00                      231294.0   \n",
       "2016                              7465117.12                      204646.0   \n",
       "2017                              2620648.65                      249987.0   \n",
       "\n",
       "      Total Customers Previous Year  New Customers  Lost Customers  \n",
       "2015                            0.0       231294.0        231294.0  \n",
       "2016                       231294.0       145062.0        171710.0  \n",
       "2017                       204646.0       228262.0        354631.0  "
      ]
     },
     "execution_count": 100,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "### Combine all Dataframes into one big one!\n",
    "\n",
    "#frames = [df1, df2, df3]\n",
    "\n",
    "#result = pd.concat(frames)\n",
    "\n",
    "dfs = [total_rev, new_rev, ex_growth, attrition, ex_cust_rev, ex_cust_rev_p, total_cust, total_cust_prev, new_cust, lost_cust]\n",
    "result = pd.concat(dfs)\n",
    "result = result.fillna(0)\n",
    "result = result.transpose()\n",
    "result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 123,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[Text(0.5, 0, 'Total Revenue'),\n",
       " Text(1.5, 0, 'New Customer Revenue'),\n",
       " Text(2.5, 0, 'Existing Customer Growth'),\n",
       " Text(3.5, 0, 'Attrition'),\n",
       " Text(4.5, 0, 'Existing Customer Revenue (Current Year)'),\n",
       " Text(5.5, 0, 'Existing Customer Revenue (Prior Year)'),\n",
       " Text(6.5, 0, 'Total Customers Current Year'),\n",
       " Text(7.5, 0, 'Total Customers Previous Year'),\n",
       " Text(8.5, 0, 'New Customers'),\n",
       " Text(9.5, 0, 'Lost Customers')]"
      ]
     },
     "execution_count": 123,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "### This matrix helps us visualize which metrics We calculated are correlated with each other\n",
    "# I am using this to see if there are going to be any clear trends within the data.  \n",
    "# *If there is high correlation between two metrics, I will see the trend more easily this way* \n",
    "\n",
    "import seaborn as sns\n",
    "\n",
    "corr = result.corr()\n",
    "ax = sns.heatmap(\n",
    "    corr, \n",
    "    vmin=-1, vmax=1, center=0,\n",
    "    cmap=sns.diverging_palette(20, 220, n=200),\n",
    "    square=True\n",
    ")\n",
    "\n",
    "ax.set_xticklabels(\n",
    "    ax.get_xticklabels(),\n",
    "    rotation=45,\n",
    "    horizontalalignment='right'\n",
    ")\n",
    "\n",
    "# Some interesting parts of the matrix are:\n",
    "    # Total Customers and Total Revenue for a year is highly correlated with the number of lost customers in that same year,\n",
    "      # which is the opposite of what you may assume\n",
    "    # Total Customers in the previous year highly correlates with Revenue coming from New Customers in that year.\n",
    "      # This makes sense because when there are more new customers, there will likely be more total customers, meaning a potential for greater revenue in that year.\n",
    "    # Attrition is inversely correlated with lsot customers, Total Customers, and Total Revenue.\n",
    "    # New Customers is inversely correlated with Existing Customer Revenue for both the current and prior year.\n",
    "      # New Customers are not factored into the calculations of Existing Customer Revenue, so they will likely not be correlated, or inversely correlated if revenues change\n",
    "        "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 118,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "  \n",
    "plt.plot(result.index, result['New Customers'], label = \"New\")\n",
    "plt.plot(result.index, result['Lost Customers'], label = \"Lost\")\n",
    "plt.legend()\n",
    "plt.show()\n",
    "\n",
    "### This plot shows that every year, the amount of customers that are new never exceed the amount of customers we lose.\n",
    "# This looks bad for future growth, so let's see if growth changes over time"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 122,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAXcAAAD4CAYAAAAXUaZHAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjIsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+WH4yJAAAgAElEQVR4nO3deXxU5dnG8d9NSAhL2EJYw6qAsicEcK0gKmh9lWpBFFooWguCorVatLWWVqu11FoqorxVyythE7CgVaui1rpLFraETZYQiBBAdgNZnvePjBAhQJKZ4cxMru/nA3P2c83k5J6T58x5xpxziIhIZKnhdQAREQk8FXcRkQik4i4iEoFU3EVEIpCKu4hIBKrpdQCAJk2auHbt2nkdQ0QkrKSlpe1yziWUNy8kinu7du1YtmyZ1zFERMKKmW051Tw1y4iIRCAVdxGRCKTiLiISgUKizb08hYWF5ObmUlBQ4HUUOYXY2FgSExOJjo72OoqInCBki3tubi5xcXG0a9cOM/M6jpzAOcfu3bvJzc2lffv2XscRkROEbLNMQUEB8fHxKuwhysyIj4/XX1YiIeqMxd3MXjCznWa2qsy0P5nZGjNbYWavmFnDMvMeMLMNZrbWzAb5E06FPbTp5yMSuipy5v4PYPAJ094GujnnegDrgAcAzKwLMBzo6lvnGTOLClhaEZEIMvPjzXy8YVdQtn3G4u6c+wDYc8K0t5xzRb7RT4FE3/D1wFzn3BHn3CZgA9A3gHnPmt27d9OrVy969epF8+bNadWq1bHxo0ePfmfZp556isOHD59xm/379y/3Zq3+/fvTuXNnevbsSZ8+fcjMzAzY8xCR0PTxhl1MfnU185ZtDcr2A9HmPgZ4wzfcCiibNNc37SRmdruZLTOzZfn5+QGIEVjx8fFkZmaSmZnJ2LFjueeee46Nx8TEfGfZihb300lNTWX58uXccccd3HfffX5tS0RC21f7CrhzTgYdEurxhx90D8o+/CruZvYroAhI/XZSOYuV+1VPzrkZzrkU51xKQkK5XSOEnKVLl5KUlET37t0ZM2YMR44cYerUqWzfvp0BAwYwYMAAAMaNG0dKSgpdu3bl4YcfrtQ+LrzwQrZt2wbAoUOHGDNmDH369CEpKYnFixcD0K9fP1avXn1snf79+5OWlnbK5f/xj39www03MHjwYDp27Mj9999/bN169eodG16wYAGjR48GID8/nxtvvJE+ffrQp08fPvroo8q/YCJyksLiEsbPTuebwmKeHZlM3VrB+dBilbdqZqOAa4GB7vh39eUCrcsslghsr3q8UpNfXU3W9v3+buY7urSsz8P/07XCyxcUFDB69GiWLl1Kp06d+PGPf8z06dO5++67efLJJ3nvvfdo0qQJAI8++iiNGzemuLiYgQMHsmLFCnr06FGh/bz55psMGTLk2HYuv/xyXnjhBfbu3Uvfvn254oorGD58OPPnz2fy5Mnk5eWxfft2evfuzYMPPlju8gCZmZlkZGRQq1YtOnfuzJ133knr1q1PmWPixIncc889XHLJJeTk5DBo0CCys7Mr/HqJSPkee30NaVu+ZurNSZzbNC5o+6lScTezwcAvgcucc2XbI5YAs83sSaAl0BH43O+UIaC4uJj27dvTqVMnAEaNGsW0adO4++67T1p2/vz5zJgxg6KiIvLy8sjKyjpjcR8xYgSHDh2iuLiY9PR0AN566y2WLFnClClTgNI3mJycHIYNG8aVV17J5MmTmT9/PkOHDj3t8gADBw6kQYMGAHTp0oUtW7actri/8847ZGVlHRvfv38/Bw4cIC4ueAejSKT714o8XvhoE6Mvasd1PVsGdV9nLO5mNgfoDzQxs1zgYUo/HVMLeNv3cbhPnXNjnXOrzWw+kEVpc81451yxvyErc4YdLHXr1q3Qcps2bWLKlCl88cUXNGrUiNGjR1fos+Cpqan07NmTSZMmMX78eBYtWoRzjoULF9K5c+eTlo+Pj2fFihXMmzeP5557DuCUy3/22WfUqlXr2HhUVBRFRaXXw8t+nLFszpKSEj755BNq165doectIqe3YedB7l+wnOQ2DXnwmvODvr+KfFrmZudcC+dctHMu0Tn3vHPuXOdca+dcL9+/sWWWf9Q5d45zrrNz7o3TbTucFBQUsHnzZjZs2ADASy+9xGWXXQZAXFwcBw4cAErPcOvWrUuDBg3YsWMHb7xR8ZcgOjqaRx55hE8//ZTs7GwGDRrE3/72N75t9crIyDi27PDhw3niiSfYt28f3buXXpA53fKn0qxZM7KzsykpKeGVV145Nv2qq67i6aefPjauT/CIVN2hI0WMm5VGregopo1IJqZm8O8fDdk7VENNbGwsL774IkOHDqV79+7UqFGD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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.plot(result.index, result['Existing Customer Growth'], label = \"Total Revenue\")\n",
    "#plt.plot(result.index, result['Total Revenue'], label = \"Total Revenue\")\n",
    "plt.legend()\n",
    "plt.show()\n",
    "\n",
    "#  When graphing customer growth, We see the complete opposite of the trend in the last graph.\n",
    "#     An idea for that is existing customers are spending more than a new customer typically.\n",
    "#     This makes sense that a loyal customer is more likely to spend more than a new customer who never used the product before."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
