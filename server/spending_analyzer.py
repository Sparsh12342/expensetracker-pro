import pandas as pd
import re
from typing import Dict, List, Tuple
from collections import defaultdict, Counter
import requests
from bs4 import BeautifulSoup
import time
import random

class SpendingAnalyzer:
    def __init__(self):
        self.merchant_patterns = {
            'restaurants': [
                'CHIPOTLE', 'MCDONALDS', 'STARBUCKS', 'SUBWAY', 'PIZZA HUT',
                'BLAZE PIZZA', 'CHICK-FIL-A', 'TACO BELL', 'BURGER KING',
                'WENDYS', 'KFC', 'DOMINOS', 'PAPA JOHNS', 'OLIVE GARDEN',
                'APPLEBEES', 'CHILIS', 'OUTBACK', 'RED LOBSTER'
            ],
            'groceries': [
                'WALMART', 'TARGET', 'COSTCO', 'WHOLE FOODS', 'TRADER JOES',
                'SAFEWAY', 'KROGER', 'SHOPRITE', 'STOP & SHOP', 'ACME',
                'H MART', 'BUTLER FOOD', 'KNIGHTS DELI'
            ],
            'transportation': [
                'UBER', 'LYFT', 'GAS STATION', 'EXXON', 'SHELL', 'BP',
                'CHEVRON', 'MOBIL', 'PARKING', 'METRO', 'NJT'
            ],
            'entertainment': [
                'NETFLIX', 'SPOTIFY', 'AMAZON PRIME', 'MOVIE', 'CINEMA',
                'THEATER', 'CONCERT', 'GAME', 'STEAM', 'PLAYSTATION'
            ],
            'shopping': [
                'AMAZON', 'MACYS', 'BEST BUY', 'SEPHORA', 'ULTA', 'FOREVER21',
                'ZARA', 'H&M', 'NORDSTROM', 'KOHLS', 'JCPENNEY'
            ],
            'health': [
                'CVS', 'WALGREENS', 'RITE AID', 'DOCTOR', 'DENTAL', 'GYM',
                'PHARMACY', 'HOSPITAL', 'CLINIC'
            ]
        }
        
        self.price_comparison_sites = {
            'amazon': 'https://www.amazon.com/s?k={query}',
            'walmart': 'https://www.walmart.com/search?q={query}',
            'target': 'https://www.target.com/s?searchTerm={query}',
            'google_shopping': 'https://www.google.com/search?tbm=shop&q={query}'
        }

    def analyze_spending_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze spending patterns and identify top expense categories"""
        if df.empty:
            return {}
        
        # Ensure Amount is numeric
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df = df.dropna(subset=['Amount'])
        
        # Focus on expenses - handle both positive and negative amounts
        # If amounts are negative, they're expenses; if positive, they're also expenses in our format
        expenses = df[df['Amount'] != 0].copy()  # Exclude zero amounts
        # Make all amounts positive for analysis
        expenses['Amount'] = expenses['Amount'].abs()
        
        # Categorize transactions
        expenses['Category'] = expenses['Description'].apply(self._categorize_transaction)
        
        # Group by category and calculate totals
        category_totals = expenses.groupby('Category').agg({
            'Amount': ['sum', 'count', 'mean'],
            'Description': lambda x: list(x.unique())[:5]  # Top 5 descriptions
        }).round(2)
        
        # Flatten column names
        category_totals.columns = ['Total_Spent', 'Transaction_Count', 'Avg_Amount', 'Top_Descriptions']
        category_totals = category_totals.sort_values('Total_Spent', ascending=False)
        
        # Get top spending categories
        top_categories = category_totals.head(5).to_dict('index')
        
        # Analyze individual merchants
        merchant_analysis = self._analyze_merchants(expenses)
        
        return {
            'top_categories': top_categories,
            'merchant_analysis': merchant_analysis,
            'total_expenses': expenses['Amount'].sum(),
            'avg_transaction': expenses['Amount'].mean(),
            'total_transactions': len(expenses)
        }

    def _categorize_transaction(self, description: str) -> str:
        """Categorize transaction based on description"""
        desc_upper = str(description).upper()
        
        for category, patterns in self.merchant_patterns.items():
            for pattern in patterns:
                if pattern in desc_upper:
                    return category.title()
        
        return 'Other'

    def _analyze_merchants(self, expenses: pd.DataFrame) -> Dict:
        """Analyze spending by merchant using pattern matching"""
        merchant_spending = defaultdict(lambda: {'total': 0, 'count': 0, 'descriptions': set(), 'categories': set()})
        
        # Comprehensive merchant patterns
        merchant_patterns = {
            'CHIPOTLE': ['CHIPOTLE'],
            'STARBUCKS': ['STARBUCKS'],
            'UBER': ['UBER'],
            'AMAZON': ['AMAZON'],
            'TARGET': ['TARGET'],
            'WALMART': ['WAL-MART', 'WALMART'],
            'COSTCO': ['COSTCO'],
            'WHOLE FOODS': ['WHOLE FOODS', 'WHOLEFDS'],
            'MACYS': ['MACYS'],
            'CVS': ['CVS'],
            'WALGREENS': ['WALGREENS'],
            '7-ELEVEN': ['7-ELEVEN'],
            'BURGER KING': ['BURGER KING'],
            'TACO BELL': ['TACO BELL'],
            'PIZZA HUT': ['PIZZA HUT'],
            'DOMINOS': ['DOMINOS'],
            'LITTLE CAESARS': ['LITTLE CAESARS'],
            'PAPA JOHNS': ['PAPA JOHNS'],
            'JERSEY MIKES': ['JERSEY MIKES'],
            'JIMMY JOHNS': ['JIMMY JOHNS'],
            'QUIZNOS': ['QUIZNOS'],
            'DUNKIN DONUTS': ['DUNKIN DONUTS'],
            'MCDONALDS': ['MCDONALDS'],
            'FIVE GUYS': ['FIVE GUYS'],
            'IN N OUT': ['IN N OUT'],
            'SHAKE SHACK': ['SHAKE SHACK'],
            'KFC': ['KFC'],
            'POPEYES': ['POPEYES'],
            'CHICK-FIL-A': ['CHICK-FIL-A'],
            'CHURCHS CHICKEN': ['CHURCHS CHICKEN'],
            'DEL TACO': ['DEL TACO'],
            'MOES SOUTHWEST': ['MOES SOUTHWEST'],
            'QDOBA': ['QDOBA'],
            'SUBWAY': ['SUBWAY'],
            'ALDI': ['ALDI'],
            'SPROUTS': ['SPROUTS'],
            'SAFEWAY': ['SAFEWAY'],
            'KROGER': ['KROGER'],
            'PUBLIX': ['PUBLIX'],
            'WINN DIXIE': ['WINN DIXIE'],
            'H MART': ['H MART'],
            'EBAY': ['EBAY'],
            'KOHLS': ['KOHLS'],
            'JCPENNEY': ['JCPENNEY'],
            'TJ MAXX': ['TJ MAXX'],
            'MARSHALLS': ['MARSHALLS'],
            'ROSS': ['ROSS'],
            'BURLINGTON': ['BURLINGTON'],
            'H&M': ['H&M'],
            'ZARA': ['ZARA'],
            'NORDSTROM': ['NORDSTROM'],
            'NIKE': ['NIKE'],
            'ADIDAS': ['ADIDAS'],
            'PUMA': ['PUMA'],
            'NEW BALANCE': ['NEW BALANCE'],
            'DSW': ['DSW'],
            'FOOT LOCKER': ['FOOT LOCKER'],
            'HULU': ['HULU'],
            'DISNEY+': ['DISNEY+'],
            'AMAZON PRIME': ['AMAZON PRIME'],
            'APPLE MUSIC': ['APPLE MUSIC'],
            'YOUTUBE MUSIC': ['YOUTUBE MUSIC'],
            'AMAZON MUSIC': ['AMAZON MUSIC'],
            'PANDORA': ['PANDORA'],
            'REGAL': ['REGAL'],
            'AMC': ['AMC'],
            'CIRCLE K': ['CIRCLE K'],
            'SHEETZ': ['SHEETZ'],
            'SPEEDWAY': ['SPEEDWAY'],
            'CASEYS': ['CASEYS'],
            'LOVES': ['LOVES'],
            'PILOT': ['PILOT'],
            'FLYING J': ['FLYING J'],
            'NETFLIX': ['NETFLIX'],
            'SPOTIFY': ['SPOTIFY'],
            'APPLE': ['APPLE'],
            'GOOGLE': ['GOOGLE'],
            'MICROSOFT': ['MICROSOFT'],
            'FACEBOOK': ['FACEBOOK'],
            'INSTAGRAM': ['INSTAGRAM'],
            'TWITTER': ['TWITTER'],
            'LINKEDIN': ['LINKEDIN'],
            'YOUTUBE': ['YOUTUBE'],
            'TIKTOK': ['TIKTOK'],
            'SNAPCHAT': ['SNAPCHAT'],
            'DISCORD': ['DISCORD'],
            'TWITCH': ['TWITCH'],
            'REDDIT': ['REDDIT'],
            'PINTEREST': ['PINTEREST'],
            'TUMBLR': ['TUMBLR'],
            'MEDIUM': ['MEDIUM'],
            'QUORA': ['QUORA'],
            'STACKOVERFLOW': ['STACKOVERFLOW'],
            'GITHUB': ['GITHUB'],
            'GITLAB': ['GITLAB'],
            'BITBUCKET': ['BITBUCKET'],
            'JIRA': ['JIRA'],
            'CONFLUENCE': ['CONFLUENCE'],
            'SLACK': ['SLACK'],
            'TEAMS': ['TEAMS'],
            'ZOOM': ['ZOOM'],
            'SKYPE': ['SKYPE'],
            'WHATSAPP': ['WHATSAPP'],
            'TELEGRAM': ['TELEGRAM'],
            'SIGNAL': ['SIGNAL'],
            'VIBER': ['VIBER'],
            'WECHAT': ['WECHAT'],
            'LINE': ['LINE'],
            'KAKAOTALK': ['KAKAOTALK']
        }
        
        for _, row in expenses.iterrows():
            desc = str(row['Description']).upper()
            amount = row['Amount']
            
            # Try to match merchant patterns
            merchant = None
            for merchant_name, patterns in merchant_patterns.items():
                for pattern in patterns:
                    if pattern in desc:
                        merchant = merchant_name
                        break
                if merchant:
                    break
            
            # If no pattern match, try to extract from first word
            if not merchant:
                words = desc.split()
                if len(words) >= 1:
                    merchant = words[0]
                else:
                    merchant = desc
            
            # Clean up merchant name
            merchant = merchant.strip()
            
            if len(merchant) > 2:
                # Use absolute value for spending calculation
                merchant_spending[merchant]['total'] += abs(amount)
                merchant_spending[merchant]['count'] += 1
                merchant_spending[merchant]['descriptions'].add(row['Description'])
                # Track category if available
                if 'Category' in row and pd.notna(row['Category']):
                    merchant_spending[merchant]['categories'].add(str(row['Category']))
        
        # Convert to list and sort by total spending
        merchant_list = []
        for merchant, data in merchant_spending.items():
            if data['total'] > 5:  # Lower threshold to capture more merchants
                # Get primary category (most common one)
                primary_category = 'Other'
                if data['categories']:
                    # For now, just take the first category, but could be enhanced to find most common
                    primary_category = list(data['categories'])[0]
                
                merchant_list.append({
                    'merchant': merchant,
                    'total_spent': round(data['total'], 2),
                    'transaction_count': data['count'],
                    'avg_amount': round(data['total'] / data['count'], 2),
                    'sample_descriptions': list(data['descriptions'])[:3],
                    'primary_category': primary_category,
                    'all_categories': list(data['categories'])
                })
        
        return sorted(merchant_list, key=lambda x: x['total_spent'], reverse=True)[:25]  # Return more merchants

    def find_cheaper_alternatives(self, merchant: str, category: str, avg_amount: float) -> List[Dict]:
        """Find cheaper alternatives for a specific merchant/category"""
        alternatives = []
        
        try:
            # Search for alternatives based on category
            if category.lower() == 'restaurants':
                alternatives.extend(self._find_restaurant_alternatives(merchant, avg_amount))
            elif category.lower() == 'groceries':
                alternatives.extend(self._find_grocery_alternatives(merchant, avg_amount))
            elif category.lower() == 'shopping':
                alternatives.extend(self._find_shopping_alternatives(merchant, avg_amount))
            elif category.lower() == 'transportation':
                alternatives.extend(self._find_transportation_alternatives(merchant, avg_amount))
            
        except Exception as e:
            print(f"Error finding alternatives for {merchant}: {e}")
        
        return alternatives[:3]  # Return top 3 alternatives

    def _find_restaurant_alternatives(self, merchant: str, avg_amount: float) -> List[Dict]:
        """Find cheaper restaurant alternatives"""
        alternatives = []
        
        # Define cheaper alternatives by category
        fast_casual_alternatives = {
            'CHIPOTLE': ['Qdoba', 'Moe\'s Southwest Grill', 'Baja Fresh', 'Chipotle (lunch specials)'],
            'STARBUCKS': ['Dunkin\' Donuts', 'McDonald\'s Coffee', 'Local coffee shops', 'Make coffee at home'],
            'BLAZE PIZZA': ['Domino\'s', 'Papa John\'s', 'Little Caesars', 'Frozen pizza'],
            'CHICK-FIL-A': ['Popeyes', 'KFC', 'Church\'s Chicken', 'Homemade chicken']
        }
        
        if merchant in fast_casual_alternatives:
            for alt in fast_casual_alternatives[merchant]:
                savings = avg_amount * 0.2  # Assume 20% savings
                alternatives.append({
                    'alternative': alt,
                    'estimated_savings': round(savings, 2),
                    'savings_percentage': 20,
                    'reason': f'Cheaper alternative to {merchant}',
                    'category': 'Restaurant'
                })
        
        return alternatives

    def _find_grocery_alternatives(self, merchant: str, avg_amount: float) -> List[Dict]:
        """Find cheaper grocery alternatives"""
        alternatives = []
        
        grocery_alternatives = {
            'WHOLE FOODS': ['Trader Joe\'s', 'Walmart', 'Target', 'Local grocery stores'],
            'TARGET': ['Walmart', 'Costco (bulk)', 'Local grocery stores', 'Online grocery delivery'],
            'WALMART': ['Costco (bulk)', 'Local grocery stores', 'Online grocery delivery', 'Coupon apps'],
            'COSTCO': ['Sam\'s Club', 'Bulk buying at local stores', 'Online bulk retailers']
        }
        
        if merchant in grocery_alternatives:
            for alt in grocery_alternatives[merchant]:
                savings = avg_amount * 0.15  # Assume 15% savings
                alternatives.append({
                    'alternative': alt,
                    'estimated_savings': round(savings, 2),
                    'savings_percentage': 15,
                    'reason': f'More affordable grocery option than {merchant}',
                    'category': 'Groceries'
                })
        
        return alternatives

    def _find_shopping_alternatives(self, merchant: str, avg_amount: float) -> List[Dict]:
        """Find cheaper shopping alternatives"""
        alternatives = []
        
        shopping_alternatives = {
            'AMAZON': ['Walmart.com', 'Target.com', 'eBay', 'Local stores', 'Price comparison sites'],
            'MACYS': ['Kohl\'s', 'JCPenney', 'TJ Maxx', 'Marshalls', 'Online sales'],
            'BEST BUY': ['Amazon', 'Walmart', 'Costco', 'Newegg', 'Wait for sales'],
            'SEPHORA': ['Ulta', 'Drugstore brands', 'Online beauty retailers', 'Wait for sales']
        }
        
        if merchant in shopping_alternatives:
            for alt in shopping_alternatives[merchant]:
                savings = avg_amount * 0.25  # Assume 25% savings
                alternatives.append({
                    'alternative': alt,
                    'estimated_savings': round(savings, 2),
                    'savings_percentage': 25,
                    'reason': f'More affordable shopping option than {merchant}',
                    'category': 'Shopping'
                })
        
        return alternatives

    def _find_transportation_alternatives(self, merchant: str, avg_amount: float) -> List[Dict]:
        """Find cheaper transportation alternatives"""
        alternatives = []
        
        if 'UBER' in merchant or 'LYFT' in merchant:
            alternatives.extend([
                {
                    'alternative': 'Public transportation',
                    'estimated_savings': round(avg_amount * 0.7, 2),
                    'savings_percentage': 70,
                    'reason': 'Much cheaper than ride-sharing',
                    'category': 'Transportation'
                },
                {
                    'alternative': 'Walking/Biking',
                    'estimated_savings': round(avg_amount, 2),
                    'savings_percentage': 100,
                    'reason': 'Free and healthy alternative',
                    'category': 'Transportation'
                },
                {
                    'alternative': 'Carpooling',
                    'estimated_savings': round(avg_amount * 0.5, 2),
                    'savings_percentage': 50,
                    'reason': 'Split costs with others',
                    'category': 'Transportation'
                }
            ])
        
        return alternatives

    def generate_savings_report(self, spending_analysis: Dict) -> Dict:
        """Generate comprehensive savings report based on highest spending categories"""
        report = {
            'total_potential_savings': 0,
            'savings_opportunities': [],
            'detailed_recommendations': [],
            'summary': {
                'total_expenses': spending_analysis.get('total_expenses', 0),
                'total_potential_savings': 0,
                'savings_percentage': 0,
                'opportunities_count': 0,
                'detailed_recommendations_count': 0
            }
        }
        
        # Get top spending categories
        top_categories = spending_analysis.get('top_categories', {})
        sorted_categories = sorted(top_categories.items(), key=lambda x: x[1]['Total_Spent'], reverse=True)
        
        # Generate savings opportunities for top 5 spending categories
        for category, data in sorted_categories[:5]:
            if data['Total_Spent'] > 10:  # Only analyze categories with >$10 spending
                category_opportunities = self._generate_category_savings_opportunities(category, data)
                report['savings_opportunities'].extend(category_opportunities)
        
        # Enhanced merchant-specific recommendations for top spending categories
        detailed_recommendations = self._generate_detailed_recommendations(spending_analysis)
        report['detailed_recommendations'] = detailed_recommendations
        
        # Calculate total potential savings
        for opp in report['savings_opportunities']:
            report['total_potential_savings'] += opp.get('potential_savings', 0)
        
        for rec in detailed_recommendations:
            report['total_potential_savings'] += rec.get('potential_savings', 0)
        
        # Update summary
        total_expenses = spending_analysis.get('total_expenses', 0)
        report['summary']['total_expenses'] = total_expenses
        report['summary']['total_potential_savings'] = report['total_potential_savings']
        report['summary']['savings_percentage'] = (report['total_potential_savings'] / total_expenses * 100) if total_expenses > 0 else 0
        report['summary']['opportunities_count'] = len(report['savings_opportunities'])
        report['summary']['detailed_recommendations_count'] = len(detailed_recommendations)
        
        return report
    
    def _generate_category_savings_opportunities(self, category: str, data: Dict) -> List[Dict]:
        """Generate savings opportunities for a specific category"""
        opportunities = []
        total_spent = data['Total_Spent']
        avg_amount = data['Avg_Amount']
        transaction_count = data['Transaction_Count']
        
        # Category-specific savings strategies
        if category.lower() == 'restaurants':
            opportunities.extend(self._get_restaurant_savings_opportunities(total_spent, avg_amount, transaction_count))
        elif category.lower() == 'groceries':
            opportunities.extend(self._get_grocery_savings_opportunities(total_spent, avg_amount, transaction_count))
        elif category.lower() == 'shopping':
            opportunities.extend(self._get_shopping_savings_opportunities(total_spent, avg_amount, transaction_count))
        elif category.lower() == 'transportation':
            opportunities.extend(self._get_transportation_savings_opportunities(total_spent, avg_amount, transaction_count))
        elif category.lower() == 'entertainment':
            opportunities.extend(self._get_entertainment_savings_opportunities(total_spent, avg_amount, transaction_count))
        else:
            opportunities.extend(self._get_generic_savings_opportunities(category, total_spent, avg_amount, transaction_count))
        
        return opportunities
    
    def _get_restaurant_savings_opportunities(self, total_spent: float, avg_amount: float, transaction_count: int) -> List[Dict]:
        """Generate restaurant-specific savings opportunities"""
        opportunities = []
        
        # Opportunity 1: Cook at home more often
        if transaction_count > 5:
            potential_savings = total_spent * 0.3  # 30% savings by cooking at home
            opportunities.append({
                'title': 'Cook at Home More Often',
                'category': 'Restaurants',
                'current_spending': total_spent,
                'potential_savings': round(potential_savings, 2),
                'savings_percentage': 30,
                'description': f'You spent ${total_spent:.2f} on restaurants. Cooking at home 2-3 times per week could save you ${potential_savings:.2f} per month.',
                'action_items': [
                    'Meal prep on weekends',
                    'Buy groceries instead of eating out',
                    'Learn 5-10 simple recipes',
                    'Use leftovers for lunch'
                ]
            })
        
        # Opportunity 2: Use restaurant deals and coupons
        if total_spent > 50:
            potential_savings = total_spent * 0.15  # 15% savings with deals
            opportunities.append({
                'title': 'Use Restaurant Deals and Coupons',
                'category': 'Restaurants',
                'current_spending': total_spent,
                'potential_savings': round(potential_savings, 2),
                'savings_percentage': 15,
                'description': f'Use apps like Groupon, Restaurant.com, or restaurant loyalty programs to save ${potential_savings:.2f} per month.',
                'action_items': [
                    'Download restaurant apps for deals',
                    'Check Groupon for restaurant offers',
                    'Sign up for loyalty programs',
                    'Look for happy hour specials'
                ]
            })
        
        # Opportunity 3: Choose cheaper restaurant alternatives
        if avg_amount > 15:
            potential_savings = total_spent * 0.25  # 25% savings with cheaper options
            opportunities.append({
                'title': 'Choose Cheaper Restaurant Alternatives',
                'category': 'Restaurants',
                'current_spending': total_spent,
                'potential_savings': round(potential_savings, 2),
                'savings_percentage': 25,
                'description': f'Your average restaurant bill is ${avg_amount:.2f}. Consider fast-casual or local restaurants to save ${potential_savings:.2f} per month.',
                'action_items': [
                    'Try local mom-and-pop restaurants',
                    'Choose fast-casual over sit-down',
                    'Share entrees with friends',
                    'Skip drinks and desserts'
                ]
            })
        
        return opportunities
    
    def _get_grocery_savings_opportunities(self, total_spent: float, avg_amount: float, transaction_count: int) -> List[Dict]:
        """Generate grocery-specific savings opportunities"""
        opportunities = []
        
        # Opportunity 1: Use coupons and store brands
        if total_spent > 100:
            potential_savings = total_spent * 0.20  # 20% savings with coupons
            opportunities.append({
                'title': 'Use Coupons and Store Brands',
                'category': 'Groceries',
                'current_spending': total_spent,
                'potential_savings': round(potential_savings, 2),
                'savings_percentage': 20,
                'description': f'You spent ${total_spent:.2f} on groceries. Using coupons and store brands could save you ${potential_savings:.2f} per month.',
                'action_items': [
                    'Download store apps for digital coupons',
                    'Try store brand products',
                    'Plan meals around sales',
                    'Use cashback apps like Ibotta'
                ]
            })
        
        # Opportunity 2: Buy in bulk for non-perishables
        if transaction_count > 3:
            potential_savings = total_spent * 0.15  # 15% savings with bulk buying
            opportunities.append({
                'title': 'Buy in Bulk for Non-Perishables',
                'category': 'Groceries',
                'current_spending': total_spent,
                'potential_savings': round(potential_savings, 2),
                'savings_percentage': 15,
                'description': f'Buying non-perishable items in bulk could save you ${potential_savings:.2f} per month.',
                'action_items': [
                    'Join Costco or Sam\'s Club',
                    'Buy toilet paper, paper towels in bulk',
                    'Stock up on canned goods during sales',
                    'Share bulk purchases with friends'
                ]
            })
        
        return opportunities
    
    def _get_shopping_savings_opportunities(self, total_spent: float, avg_amount: float, transaction_count: int) -> List[Dict]:
        """Generate shopping-specific savings opportunities"""
        opportunities = []
        
        # Opportunity 1: Wait for sales and use price comparison
        if total_spent > 50:
            potential_savings = total_spent * 0.30  # 30% savings with sales
            opportunities.append({
                'title': 'Wait for Sales and Compare Prices',
                'category': 'Shopping',
                'current_spending': total_spent,
                'potential_savings': round(potential_savings, 2),
                'savings_percentage': 30,
                'description': f'You spent ${total_spent:.2f} on shopping. Waiting for sales and comparing prices could save you ${potential_savings:.2f} per month.',
                'action_items': [
                    'Use price comparison websites',
                    'Wait for Black Friday, Cyber Monday sales',
                    'Sign up for store newsletters',
                    'Use browser extensions like Honey'
                ]
            })
        
        return opportunities
    
    def _get_transportation_savings_opportunities(self, total_spent: float, avg_amount: float, transaction_count: int) -> List[Dict]:
        """Generate transportation-specific savings opportunities"""
        opportunities = []
        
        # Opportunity 1: Use public transportation or carpool
        if total_spent > 30:
            potential_savings = total_spent * 0.40  # 40% savings with alternatives
            opportunities.append({
                'title': 'Use Public Transportation or Carpool',
                'category': 'Transportation',
                'current_spending': total_spent,
                'potential_savings': round(potential_savings, 2),
                'savings_percentage': 40,
                'description': f'You spent ${total_spent:.2f} on transportation. Using public transit or carpooling could save you ${potential_savings:.2f} per month.',
                'action_items': [
                    'Get a monthly transit pass',
                    'Find carpool partners',
                    'Use bike-sharing programs',
                    'Walk for short distances'
                ]
            })
        
        return opportunities
    
    def _get_entertainment_savings_opportunities(self, total_spent: float, avg_amount: float, transaction_count: int) -> List[Dict]:
        """Generate entertainment-specific savings opportunities"""
        opportunities = []
        
        # Opportunity 1: Use free entertainment options
        if total_spent > 25:
            potential_savings = total_spent * 0.50  # 50% savings with free options
            opportunities.append({
                'title': 'Use Free Entertainment Options',
                'category': 'Entertainment',
                'current_spending': total_spent,
                'potential_savings': round(potential_savings, 2),
                'savings_percentage': 50,
                'description': f'You spent ${total_spent:.2f} on entertainment. Using free options could save you ${potential_savings:.2f} per month.',
                'action_items': [
                    'Visit free museums and parks',
                    'Use library for books and movies',
                    'Attend free community events',
                    'Host game nights at home'
                ]
            })
        
        return opportunities
    
    def _get_generic_savings_opportunities(self, category: str, total_spent: float, avg_amount: float, transaction_count: int) -> List[Dict]:
        """Generate generic savings opportunities for any category"""
        opportunities = []
        
        # Opportunity 1: Reduce frequency
        if transaction_count > 3:
            potential_savings = total_spent * 0.20  # 20% savings by reducing frequency
            opportunities.append({
                'title': f'Reduce {category} Spending Frequency',
                'category': category,
                'current_spending': total_spent,
                'potential_savings': round(potential_savings, 2),
                'savings_percentage': 20,
                'description': f'You spent ${total_spent:.2f} on {category.lower()}. Reducing frequency could save you ${potential_savings:.2f} per month.',
                'action_items': [
                    'Set a monthly budget for this category',
                    'Track spending to identify patterns',
                    'Find free alternatives',
                    'Wait 24 hours before making purchases'
                ]
            })
        
        return opportunities

    def _generate_detailed_recommendations(self, spending_analysis: Dict) -> List[Dict]:
        """Generate detailed, merchant-specific recommendations"""
        recommendations = []
        
        # Comprehensive merchant alternatives database
        merchant_alternatives = {
            # Fast Food & Casual Dining
            'CHIPOTLE': {
                'alternatives': ['Taco Bell', 'Qdoba', 'Moe\'s Southwest Grill', 'Local Mexican restaurants', 'Make burrito bowls at home'],
                'savings_potential': 0.35,
                'reasoning': 'Taco Bell offers similar flavors at 30-40% lower prices. Local Mexican restaurants often have better value and authentic flavors.'
            },
            'TACO BELL': {
                'alternatives': ['Del Taco', 'Local Mexican places', 'Make tacos at home', 'Chipotle (occasionally)', 'Qdoba'],
                'savings_potential': 0.2,
                'reasoning': 'Del Taco offers similar items at lower prices. Making tacos at home is much cheaper and healthier.'
            },
            'DEL TACO': {
                'alternatives': ['Taco Bell', 'Local Mexican places', 'Make tacos at home', 'Qdoba', 'Moe\'s Southwest Grill'],
                'savings_potential': 0.15,
                'reasoning': 'Taco Bell often has better deals. Local Mexican places offer better value and taste.'
            },
            'QDOBA': {
                'alternatives': ['Chipotle', 'Moe\'s Southwest Grill', 'Local Mexican restaurants', 'Make burrito bowls at home', 'Taco Bell'],
                'savings_potential': 0.25,
                'reasoning': 'Chipotle often has better deals. Local Mexican restaurants offer better value and authentic flavors.'
            },
            'MOES SOUTHWEST GRILL': {
                'alternatives': ['Chipotle', 'Qdoba', 'Local Mexican restaurants', 'Make burrito bowls at home', 'Taco Bell'],
                'savings_potential': 0.2,
                'reasoning': 'Chipotle and Qdoba often have better deals. Local Mexican restaurants offer better value.'
            },
            'STARBUCKS': {
                'alternatives': ['Dunkin\' Donuts', 'McDonald\'s Coffee', 'Local coffee shops', 'Make coffee at home', 'Gas station coffee'],
                'savings_potential': 0.5,
                'reasoning': 'Dunkin\' Donuts is 40-50% cheaper. Making coffee at home costs 90% less. Local shops often have better prices and quality.'
            },
            'MCDONALDS': {
                'alternatives': ['Burger King', 'Wendy\'s', 'Local burger joints', 'Make burgers at home', 'Five Guys (occasionally)'],
                'savings_potential': 0.2,
                'reasoning': 'Burger King and Wendy\'s often have better deals. Local burger joints offer better value and quality.'
            },
            'SUBWAY': {
                'alternatives': ['Jersey Mike\'s', 'Local delis', 'Make sandwiches at home', 'Jimmy John\'s', 'Quiznos'],
                'savings_potential': 0.4,
                'reasoning': 'Local delis often have better prices and fresher ingredients. Making sandwiches at home is 70% cheaper.'
            },
            'PIZZA HUT': {
                'alternatives': ['Domino\'s', 'Little Caesars', 'Local pizza places', 'Frozen pizza at home', 'Papa John\'s'],
                'savings_potential': 0.3,
                'reasoning': 'Domino\'s and Little Caesars often have better deals. Local pizza places offer better value and taste.'
            },
            'CHICK-FIL-A': {
                'alternatives': ['Popeyes', 'KFC', 'Local chicken restaurants', 'Make chicken at home', 'Zaxby\'s'],
                'savings_potential': 0.25,
                'reasoning': 'Popeyes and KFC offer similar quality at lower prices. Local chicken restaurants often have better deals.'
            },
            'BLAZE PIZZA': {
                'alternatives': ['Mod Pizza', 'Pie Five', 'Local pizza joints', 'Make pizza at home', 'Domino\'s'],
                'savings_potential': 0.3,
                'reasoning': 'Mod Pizza and Pie Five offer similar build-your-own concepts at lower prices.'
            },
            'TACO BELL': {
                'alternatives': ['Del Taco', 'Local Mexican places', 'Make tacos at home', 'Chipotle (occasionally)', 'Qdoba'],
                'savings_potential': 0.2,
                'reasoning': 'Del Taco offers similar items at lower prices. Making tacos at home is much cheaper and healthier.'
            },
            'POPEYES': {
                'alternatives': ['KFC', 'Chick-fil-A', 'Local fried chicken', 'Make fried chicken at home', 'Church\'s Chicken'],
                'savings_potential': 0.2,
                'reasoning': 'KFC often has better deals. Local fried chicken places offer better value and taste.'
            },
            
            # Grocery Stores
            'WHOLE FOODS': {
                'alternatives': ['Trader Joe\'s', 'Sprouts', 'Local organic stores', 'Regular grocery stores', 'Costco (organic section)'],
                'savings_potential': 0.4,
                'reasoning': 'Trader Joe\'s offers similar organic products at 30-40% lower prices. Regular grocery stores have organic sections at much lower prices.'
            },
            'TARGET': {
                'alternatives': ['Walmart', 'Costco (bulk)', 'Local grocery stores', 'Online grocery delivery', 'Aldi'],
                'savings_potential': 0.2,
                'reasoning': 'Walmart is typically 15-20% cheaper for groceries. Costco offers better bulk deals.'
            },
            'WAL-MART': {
                'alternatives': ['Costco (bulk)', 'Local grocery stores', 'Online grocery delivery', 'Aldi', 'Grocery outlet stores'],
                'savings_potential': 0.15,
                'reasoning': 'Costco offers better bulk deals. Local grocery stores often have better produce and sales.'
            },
            'COSTCO': {
                'alternatives': ['Sam\'s Club', 'Bulk buying at local stores', 'Online bulk retailers', 'BJ\'s Wholesale', 'Local warehouse stores'],
                'savings_potential': 0.1,
                'reasoning': 'Sam\'s Club often has similar prices. Local stores may have better deals on specific items.'
            },
            'STOP & SHOP': {
                'alternatives': ['ShopRite', 'Acme', 'Local grocery stores', 'Walmart', 'Aldi'],
                'savings_potential': 0.2,
                'reasoning': 'ShopRite and Acme often have better sales. Local grocery stores offer better produce and prices.'
            },
            'SHOPRITE': {
                'alternatives': ['Stop & Shop', 'Acme', 'Local grocery stores', 'Walmart', 'Aldi'],
                'savings_potential': 0.15,
                'reasoning': 'Local grocery stores often have better deals and fresher produce.'
            },
            'ACME': {
                'alternatives': ['ShopRite', 'Stop & Shop', 'Local grocery stores', 'Walmart', 'Aldi'],
                'savings_potential': 0.2,
                'reasoning': 'ShopRite and Stop & Shop often have better sales and prices.'
            },
            
            # Shopping & Retail
            'AMAZON': {
                'alternatives': ['Walmart.com', 'Target.com', 'eBay', 'Local stores', 'Price comparison sites'],
                'savings_potential': 0.15,
                'reasoning': 'Walmart.com and Target.com often have better prices. Local stores may have sales and no shipping costs.'
            },
            'MACYS': {
                'alternatives': ['Kohl\'s', 'TJ Maxx', 'Marshalls', 'Online sales', 'Outlet stores'],
                'savings_potential': 0.3,
                'reasoning': 'Kohl\'s has better sales and rewards. TJ Maxx and Marshalls offer designer items at 50-70% off.'
            },
            'BEST BUY': {
                'alternatives': ['Amazon', 'Walmart', 'Costco', 'Newegg', 'Wait for sales'],
                'savings_potential': 0.2,
                'reasoning': 'Amazon often has better prices. Costco offers extended warranties and better deals.'
            },
            'ULTA': {
                'alternatives': ['Sephora', 'CVS', 'Walgreens', 'Online beauty stores', 'Target beauty section'],
                'savings_potential': 0.25,
                'reasoning': 'CVS and Walgreens often have better sales and rewards. Online beauty stores offer better deals.'
            },
            'SEPHORA': {
                'alternatives': ['Ulta', 'CVS', 'Walgreens', 'Online beauty stores', 'Target beauty section'],
                'savings_potential': 0.25,
                'reasoning': 'Ulta often has better sales and rewards. Drugstore brands offer similar quality at lower prices.'
            },
            'FOREVER21': {
                'alternatives': ['H&M', 'Zara', 'TJ Maxx', 'Thrift stores', 'Online fast fashion'],
                'savings_potential': 0.4,
                'reasoning': 'H&M and Zara offer better quality. Thrift stores and TJ Maxx offer designer items at much lower prices.'
            },
            'FOOT LOCKER': {
                'alternatives': ['Nike Outlet', 'Adidas Outlet', 'DSW', 'Online shoe stores', 'Local shoe stores'],
                'savings_potential': 0.3,
                'reasoning': 'Outlet stores offer the same brands at 30-50% off. DSW has better sales and rewards.'
            },
            
            # Transportation
            'UBER': {
                'alternatives': ['Lyft', 'Public transit', 'Walking', 'Biking', 'Carpooling'],
                'savings_potential': 0.6,
                'reasoning': 'Public transit costs 80-90% less. Walking and biking are free and healthy. Lyft often has better deals.'
            },
            'LYFT': {
                'alternatives': ['Uber', 'Public transit', 'Walking', 'Biking', 'Carpooling'],
                'savings_potential': 0.6,
                'reasoning': 'Public transit costs 80-90% less. Walking and biking are free and healthy. Uber often has better deals.'
            },
            
            # Entertainment
            'NETFLIX': {
                'alternatives': ['Hulu', 'Disney+', 'Amazon Prime', 'Free streaming services', 'Library movies'],
                'savings_potential': 0.3,
                'reasoning': 'Hulu and Disney+ offer different content at similar prices. Free streaming services like Tubi and Crackle offer many movies and shows.'
            },
            'SPOTIFY': {
                'alternatives': ['Apple Music', 'YouTube Music', 'Free music services', 'Amazon Music', 'Pandora'],
                'savings_potential': 0.2,
                'reasoning': 'YouTube Music offers similar features. Free services like Spotify Free and Pandora offer music with ads.'
            },
            'RUTGERS CINEMA': {
                'alternatives': ['AMC', 'Regal', 'Streaming movies at home', 'Local theaters', 'Drive-in theaters'],
                'savings_potential': 0.4,
                'reasoning': 'AMC and Regal often have better deals and rewards. Streaming at home costs much less per movie.'
            },
            'AMC': {
                'alternatives': ['Regal', 'Local theaters', 'Streaming at home', 'Drive-in theaters', 'Matinee showings'],
                'savings_potential': 0.3,
                'reasoning': 'Regal often has better deals. Matinee showings are 30-40% cheaper. Streaming at home is much more cost-effective.'
            },
            
            # Convenience & Pharmacy
            '7-ELEVEN': {
                'alternatives': ['Wawa', 'Local convenience stores', 'Gas station stores', 'Grocery stores', 'Dollar stores'],
                'savings_potential': 0.2,
                'reasoning': 'Wawa often has better prices and quality. Local convenience stores may have better deals. Grocery stores are much cheaper for snacks and drinks.'
            },
            'WAWA': {
                'alternatives': ['7-Eleven', 'Sheetz', 'Local convenience stores', 'Gas station stores', 'Grocery stores'],
                'savings_potential': 0.15,
                'reasoning': 'Local convenience stores may have better deals. Grocery stores are much cheaper for snacks and drinks.'
            },
            'CVS': {
                'alternatives': ['Walgreens', 'Rite Aid', 'Local pharmacies', 'Walmart pharmacy', 'Online pharmacies'],
                'savings_potential': 0.1,
                'reasoning': 'Walgreens often has better sales and rewards. Walmart pharmacy typically has lower prices.'
            },
            'WALGREENS': {
                'alternatives': ['CVS', 'Rite Aid', 'Local pharmacies', 'Walmart pharmacy', 'Online pharmacies'],
                'savings_potential': 0.1,
                'reasoning': 'CVS often has better sales and rewards. Walmart pharmacy typically has lower prices.'
            },
            
            # Additional Fast Food & Casual Dining
            'BURGER KING': {
                'alternatives': ['McDonald\'s', 'Wendy\'s', 'Local burger joints', 'Make burgers at home', 'Five Guys (occasionally)'],
                'savings_potential': 0.2,
                'reasoning': 'McDonald\'s and Wendy\'s often have better deals. Local burger joints offer better value and quality.'
            },
            'WENDYS': {
                'alternatives': ['McDonald\'s', 'Burger King', 'Local burger joints', 'Make burgers at home', 'Five Guys (occasionally)'],
                'savings_potential': 0.2,
                'reasoning': 'McDonald\'s and Burger King often have better deals. Local burger joints offer better value and quality.'
            },
            'KFC': {
                'alternatives': ['Popeyes', 'Chick-fil-A', 'Local chicken restaurants', 'Make chicken at home', 'Church\'s Chicken'],
                'savings_potential': 0.2,
                'reasoning': 'Popeyes and Chick-fil-A offer similar quality at lower prices. Local chicken restaurants often have better deals.'
            },
            'DOMINOS': {
                'alternatives': ['Pizza Hut', 'Little Caesars', 'Local pizza places', 'Frozen pizza at home', 'Papa John\'s'],
                'savings_potential': 0.3,
                'reasoning': 'Little Caesars often has better deals. Local pizza places offer better value and taste.'
            },
            'LITTLE CAESARS': {
                'alternatives': ['Domino\'s', 'Pizza Hut', 'Local pizza places', 'Frozen pizza at home', 'Papa John\'s'],
                'savings_potential': 0.2,
                'reasoning': 'Domino\'s and Pizza Hut often have better deals. Local pizza places offer better value and taste.'
            },
            'PAPA JOHNS': {
                'alternatives': ['Domino\'s', 'Pizza Hut', 'Local pizza places', 'Frozen pizza at home', 'Little Caesars'],
                'savings_potential': 0.3,
                'reasoning': 'Domino\'s and Pizza Hut often have better deals. Local pizza places offer better value and taste.'
            },
            'JERSEY MIKES': {
                'alternatives': ['Subway', 'Local delis', 'Make sandwiches at home', 'Jimmy John\'s', 'Quiznos'],
                'savings_potential': 0.2,
                'reasoning': 'Subway often has better deals. Local delis offer better prices and fresher ingredients.'
            },
            'JIMMY JOHNS': {
                'alternatives': ['Subway', 'Jersey Mike\'s', 'Local delis', 'Make sandwiches at home', 'Quiznos'],
                'savings_potential': 0.2,
                'reasoning': 'Subway and Jersey Mike\'s often have better deals. Local delis offer better prices and fresher ingredients.'
            },
            'QUIZNOS': {
                'alternatives': ['Subway', 'Jersey Mike\'s', 'Local delis', 'Make sandwiches at home', 'Jimmy John\'s'],
                'savings_potential': 0.2,
                'reasoning': 'Subway and Jersey Mike\'s often have better deals. Local delis offer better prices and fresher ingredients.'
            },
            'DUNKIN DONUTS': {
                'alternatives': ['Starbucks', 'McDonald\'s Coffee', 'Local coffee shops', 'Make coffee at home', 'Gas station coffee'],
                'savings_potential': 0.3,
                'reasoning': 'McDonald\'s Coffee is often cheaper. Making coffee at home costs 90% less. Local shops often have better prices and quality.'
            },
            'MCDONALDS COFFEE': {
                'alternatives': ['Starbucks', 'Dunkin\' Donuts', 'Local coffee shops', 'Make coffee at home', 'Gas station coffee'],
                'savings_potential': 0.4,
                'reasoning': 'Dunkin\' Donuts is often cheaper. Making coffee at home costs 90% less. Local shops often have better prices and quality.'
            },
            'FIVE GUYS': {
                'alternatives': ['McDonald\'s', 'Burger King', 'Wendy\'s', 'Local burger joints', 'Make burgers at home'],
                'savings_potential': 0.4,
                'reasoning': 'McDonald\'s, Burger King, and Wendy\'s offer similar quality at much lower prices. Local burger joints offer better value.'
            },
            'IN N OUT': {
                'alternatives': ['McDonald\'s', 'Burger King', 'Wendy\'s', 'Local burger joints', 'Make burgers at home'],
                'savings_potential': 0.3,
                'reasoning': 'McDonald\'s, Burger King, and Wendy\'s offer similar quality at lower prices. Local burger joints offer better value.'
            },
            'SHAKE SHACK': {
                'alternatives': ['McDonald\'s', 'Burger King', 'Wendy\'s', 'Local burger joints', 'Make burgers at home'],
                'savings_potential': 0.4,
                'reasoning': 'McDonald\'s, Burger King, and Wendy\'s offer similar quality at much lower prices. Local burger joints offer better value.'
            },
            
            # Additional Grocery Stores
            'ALDI': {
                'alternatives': ['Walmart', 'Target', 'Local grocery stores', 'Online grocery delivery', 'Costco (bulk)'],
                'savings_potential': 0.1,
                'reasoning': 'Walmart and Target often have better deals. Local grocery stores may have better produce and sales.'
            },
            'SPROUTS': {
                'alternatives': ['Whole Foods', 'Trader Joe\'s', 'Local organic stores', 'Regular grocery stores', 'Costco (organic section)'],
                'savings_potential': 0.3,
                'reasoning': 'Trader Joe\'s offers similar organic products at lower prices. Regular grocery stores have organic sections at much lower prices.'
            },
            'SAFEWAY': {
                'alternatives': ['ShopRite', 'Stop & Shop', 'Local grocery stores', 'Walmart', 'Aldi'],
                'savings_potential': 0.2,
                'reasoning': 'ShopRite and Stop & Shop often have better sales and prices. Local grocery stores offer better produce.'
            },
            'KROGER': {
                'alternatives': ['Walmart', 'Target', 'Local grocery stores', 'Online grocery delivery', 'Aldi'],
                'savings_potential': 0.2,
                'reasoning': 'Walmart and Target often have better deals. Local grocery stores may have better produce and sales.'
            },
            'PUBLIX': {
                'alternatives': ['Walmart', 'Target', 'Local grocery stores', 'Online grocery delivery', 'Aldi'],
                'savings_potential': 0.2,
                'reasoning': 'Walmart and Target often have better deals. Local grocery stores may have better produce and sales.'
            },
            'WINN DIXIE': {
                'alternatives': ['Walmart', 'Target', 'Local grocery stores', 'Online grocery delivery', 'Aldi'],
                'savings_potential': 0.2,
                'reasoning': 'Walmart and Target often have better deals. Local grocery stores may have better produce and sales.'
            },
            'H MART': {
                'alternatives': ['Whole Foods', 'Local Asian markets', 'Regular grocery stores', 'Online Asian grocery', 'Costco'],
                'savings_potential': 0.2,
                'reasoning': 'Local Asian markets often have better prices. Regular grocery stores may have similar items at lower prices.'
            },
            
            # Additional Shopping & Retail
            'EBAY': {
                'alternatives': ['Amazon', 'Walmart.com', 'Target.com', 'Local stores', 'Price comparison sites'],
                'savings_potential': 0.1,
                'reasoning': 'Amazon, Walmart.com, and Target.com often have better prices and faster shipping. Local stores may have sales and no shipping costs.'
            },
            'KOHLS': {
                'alternatives': ['Macy\'s', 'TJ Maxx', 'Marshalls', 'Online sales', 'Outlet stores'],
                'savings_potential': 0.2,
                'reasoning': 'TJ Maxx and Marshalls offer designer items at 50-70% off. Online sales often have better deals.'
            },
            'JCPENNEY': {
                'alternatives': ['Macy\'s', 'Kohl\'s', 'TJ Maxx', 'Marshalls', 'Online sales'],
                'savings_potential': 0.25,
                'reasoning': 'TJ Maxx and Marshalls offer designer items at 50-70% off. Online sales often have better deals.'
            },
            'TJ MAXX': {
                'alternatives': ['Marshalls', 'Ross', 'Burlington', 'Online sales', 'Outlet stores'],
                'savings_potential': 0.1,
                'reasoning': 'Marshalls and Ross often have similar deals. Online sales may have better selection.'
            },
            'MARSHALLS': {
                'alternatives': ['TJ Maxx', 'Ross', 'Burlington', 'Online sales', 'Outlet stores'],
                'savings_potential': 0.1,
                'reasoning': 'TJ Maxx and Ross often have similar deals. Online sales may have better selection.'
            },
            'ROSS': {
                'alternatives': ['TJ Maxx', 'Marshalls', 'Burlington', 'Online sales', 'Outlet stores'],
                'savings_potential': 0.1,
                'reasoning': 'TJ Maxx and Marshalls often have similar deals. Online sales may have better selection.'
            },
            'BURLINGTON': {
                'alternatives': ['TJ Maxx', 'Marshalls', 'Ross', 'Online sales', 'Outlet stores'],
                'savings_potential': 0.1,
                'reasoning': 'TJ Maxx, Marshalls, and Ross often have similar deals. Online sales may have better selection.'
            },
            'H&M': {
                'alternatives': ['Zara', 'Forever 21', 'TJ Maxx', 'Thrift stores', 'Online fast fashion'],
                'savings_potential': 0.2,
                'reasoning': 'TJ Maxx offers designer items at much lower prices. Thrift stores offer great deals on quality clothing.'
            },
            'ZARA': {
                'alternatives': ['H&M', 'Forever 21', 'TJ Maxx', 'Thrift stores', 'Online fast fashion'],
                'savings_potential': 0.2,
                'reasoning': 'H&M and Forever 21 offer similar styles at lower prices. TJ Maxx offers designer items at much lower prices.'
            },
            'NORDSTROM': {
                'alternatives': ['Macy\'s', 'Kohl\'s', 'TJ Maxx', 'Marshalls', 'Online sales'],
                'savings_potential': 0.3,
                'reasoning': 'TJ Maxx and Marshalls offer designer items at 50-70% off. Online sales often have better deals.'
            },
            'NIKE': {
                'alternatives': ['Adidas', 'Puma', 'New Balance', 'Outlet stores', 'Online shoe stores'],
                'savings_potential': 0.2,
                'reasoning': 'Adidas and Puma offer similar quality at lower prices. Outlet stores offer the same brands at 30-50% off.'
            },
            'ADIDAS': {
                'alternatives': ['Nike', 'Puma', 'New Balance', 'Outlet stores', 'Online shoe stores'],
                'savings_potential': 0.2,
                'reasoning': 'Nike and Puma offer similar quality at lower prices. Outlet stores offer the same brands at 30-50% off.'
            },
            'PUMA': {
                'alternatives': ['Nike', 'Adidas', 'New Balance', 'Outlet stores', 'Online shoe stores'],
                'savings_potential': 0.2,
                'reasoning': 'Nike and Adidas offer similar quality at lower prices. Outlet stores offer the same brands at 30-50% off.'
            },
            'NEW BALANCE': {
                'alternatives': ['Nike', 'Adidas', 'Puma', 'Outlet stores', 'Online shoe stores'],
                'savings_potential': 0.2,
                'reasoning': 'Nike, Adidas, and Puma offer similar quality at lower prices. Outlet stores offer the same brands at 30-50% off.'
            },
            'DSW': {
                'alternatives': ['Foot Locker', 'Nike Outlet', 'Adidas Outlet', 'Online shoe stores', 'Local shoe stores'],
                'savings_potential': 0.2,
                'reasoning': 'Outlet stores offer the same brands at 30-50% off. Online shoe stores often have better deals.'
            },
            
            # Additional Entertainment
            'HULU': {
                'alternatives': ['Netflix', 'Disney+', 'Amazon Prime', 'Free streaming services', 'Library movies'],
                'savings_potential': 0.2,
                'reasoning': 'Netflix and Disney+ offer different content at similar prices. Free streaming services like Tubi and Crackle offer many movies and shows.'
            },
            'DISNEY+': {
                'alternatives': ['Netflix', 'Hulu', 'Amazon Prime', 'Free streaming services', 'Library movies'],
                'savings_potential': 0.2,
                'reasoning': 'Netflix and Hulu offer different content at similar prices. Free streaming services like Tubi and Crackle offer many movies and shows.'
            },
            'AMAZON PRIME': {
                'alternatives': ['Netflix', 'Hulu', 'Disney+', 'Free streaming services', 'Library movies'],
                'savings_potential': 0.2,
                'reasoning': 'Netflix, Hulu, and Disney+ offer different content at similar prices. Free streaming services like Tubi and Crackle offer many movies and shows.'
            },
            'APPLE MUSIC': {
                'alternatives': ['Spotify', 'YouTube Music', 'Free music services', 'Amazon Music', 'Pandora'],
                'savings_potential': 0.2,
                'reasoning': 'YouTube Music offers similar features. Free services like Spotify Free and Pandora offer music with ads.'
            },
            'YOUTUBE MUSIC': {
                'alternatives': ['Spotify', 'Apple Music', 'Free music services', 'Amazon Music', 'Pandora'],
                'savings_potential': 0.2,
                'reasoning': 'Spotify and Apple Music offer similar features. Free services like Spotify Free and Pandora offer music with ads.'
            },
            'AMAZON MUSIC': {
                'alternatives': ['Spotify', 'Apple Music', 'YouTube Music', 'Free music services', 'Pandora'],
                'savings_potential': 0.2,
                'reasoning': 'Spotify, Apple Music, and YouTube Music offer similar features. Free services like Spotify Free and Pandora offer music with ads.'
            },
            'PANDORA': {
                'alternatives': ['Spotify', 'Apple Music', 'YouTube Music', 'Free music services', 'Amazon Music'],
                'savings_potential': 0.2,
                'reasoning': 'Spotify, Apple Music, and YouTube Music offer similar features. Free services like Spotify Free offer music with ads.'
            },
            'REGAL': {
                'alternatives': ['AMC', 'Local theaters', 'Streaming at home', 'Drive-in theaters', 'Matinee showings'],
                'savings_potential': 0.3,
                'reasoning': 'AMC often has better deals. Matinee showings are 30-40% cheaper. Streaming at home is much more cost-effective.'
            },
            
            # Additional Convenience & Pharmacy
            'RITE AID': {
                'alternatives': ['CVS', 'Walgreens', 'Local pharmacies', 'Walmart pharmacy', 'Online pharmacies'],
                'savings_potential': 0.1,
                'reasoning': 'CVS and Walgreens often have better sales and rewards. Walmart pharmacy typically has lower prices.'
            },
            'SHEETZ': {
                'alternatives': ['Wawa', '7-Eleven', 'Local convenience stores', 'Gas station stores', 'Grocery stores'],
                'savings_potential': 0.15,
                'reasoning': 'Wawa often has better prices and quality. Local convenience stores may have better deals. Grocery stores are much cheaper for snacks and drinks.'
            },
            'SPEEDWAY': {
                'alternatives': ['7-Eleven', 'Wawa', 'Local convenience stores', 'Gas station stores', 'Grocery stores'],
                'savings_potential': 0.2,
                'reasoning': 'Wawa and 7-Eleven often have better prices and quality. Local convenience stores may have better deals. Grocery stores are much cheaper for snacks and drinks.'
            },
            'CIRCLE K': {
                'alternatives': ['7-Eleven', 'Wawa', 'Local convenience stores', 'Gas station stores', 'Grocery stores'],
                'savings_potential': 0.2,
                'reasoning': 'Wawa and 7-Eleven often have better prices and quality. Local convenience stores may have better deals. Grocery stores are much cheaper for snacks and drinks.'
            },
            'CASEYS': {
                'alternatives': ['7-Eleven', 'Wawa', 'Local convenience stores', 'Gas station stores', 'Grocery stores'],
                'savings_potential': 0.2,
                'reasoning': 'Wawa and 7-Eleven often have better prices and quality. Local convenience stores may have better deals. Grocery stores are much cheaper for snacks and drinks.'
            },
            'LOVE\'S': {
                'alternatives': ['7-Eleven', 'Wawa', 'Local convenience stores', 'Gas station stores', 'Grocery stores'],
                'savings_potential': 0.2,
                'reasoning': 'Wawa and 7-Eleven often have better prices and quality. Local convenience stores may have better deals. Grocery stores are much cheaper for snacks and drinks.'
            },
            'PILOT': {
                'alternatives': ['7-Eleven', 'Wawa', 'Local convenience stores', 'Gas station stores', 'Grocery stores'],
                'savings_potential': 0.2,
                'reasoning': 'Wawa and 7-Eleven often have better prices and quality. Local convenience stores may have better deals. Grocery stores are much cheaper for snacks and drinks.'
            },
            'FLYING J': {
                'alternatives': ['7-Eleven', 'Wawa', 'Local convenience stores', 'Gas station stores', 'Grocery stores'],
                'savings_potential': 0.2,
                'reasoning': 'Wawa and 7-Eleven often have better prices and quality. Local convenience stores may have better deals. Grocery stores are much cheaper for snacks and drinks.'
            }
        }
        
        # Generate recommendations for each merchant in the analysis
        for merchant_data in spending_analysis.get('merchant_analysis', []):
            merchant = merchant_data['merchant']
            merchant_key = merchant.upper()
            primary_category = merchant_data.get('primary_category', 'Other')
            
            # Lower threshold to get more recommendations
            if merchant_key in merchant_alternatives and merchant_data['total_spent'] > 5:
                alt_data = merchant_alternatives[merchant_key]
                potential_savings = merchant_data['total_spent'] * alt_data['savings_potential']
                
                # Generate category-specific alternatives
                category_specific_alternatives = self._get_category_specific_alternatives(
                    alt_data['alternatives'], primary_category
                )
                
                recommendations.append({
                    'merchant': merchant,
                    'current_spending': merchant_data['total_spent'],
                    'transaction_count': merchant_data['transaction_count'],
                    'avg_per_visit': merchant_data['avg_amount'],
                    'alternatives': category_specific_alternatives,
                    'potential_savings': round(potential_savings, 2),
                    'savings_percentage': round(alt_data['savings_potential'] * 100, 1),
                    'reasoning': self._get_category_specific_reasoning(alt_data['reasoning'], primary_category),
                    'specific_suggestion': f"Instead of {merchant} for {primary_category}, try: {', '.join(category_specific_alternatives[:3])}. You could save ${potential_savings:.2f} ({(alt_data['savings_potential'] * 100):.1f}%) on your ${merchant_data['total_spent']:.2f} {primary_category.lower()} spending.",
                    'sample_descriptions': merchant_data.get('sample_descriptions', [])
                })
        
        # Add generic recommendations for merchants not in our database
        for merchant_data in spending_analysis.get('merchant_analysis', []):
            merchant = merchant_data['merchant']
            merchant_key = merchant.upper()
            
            # If not in our database and spending > $10, create generic recommendation
            if merchant_key not in merchant_alternatives and merchant_data['total_spent'] > 10:
                # Determine category and create generic alternatives
                category = self._categorize_transaction(merchant)
                generic_alternatives = self._get_generic_alternatives(category)
                savings_potential = 0.15  # Default 15% savings
                potential_savings = merchant_data['total_spent'] * savings_potential
                
                recommendations.append({
                    'merchant': merchant,
                    'current_spending': merchant_data['total_spent'],
                    'transaction_count': merchant_data['transaction_count'],
                    'avg_per_visit': merchant_data['avg_amount'],
                    'alternatives': generic_alternatives,
                    'potential_savings': round(potential_savings, 2),
                    'savings_percentage': round(savings_potential * 100, 1),
                    'reasoning': f"Look for cheaper alternatives to {merchant}. Compare prices online, look for sales, or try local competitors for better deals.",
                    'specific_suggestion': f"Instead of {merchant}, try: {', '.join(generic_alternatives[:3])}. You could save ${potential_savings:.2f} ({(savings_potential * 100):.1f}%) on your ${merchant_data['total_spent']:.2f} spending.",
                    'sample_descriptions': merchant_data.get('sample_descriptions', [])
                })
        
        # Sort by potential savings (highest first)
        recommendations.sort(key=lambda x: x['potential_savings'], reverse=True)
        
        return recommendations
    
    def _get_category_specific_alternatives(self, base_alternatives: List[str], category: str) -> List[str]:
        """Generate category-specific alternatives based on the spending category"""
        category_specific = {
            'Dining': [
                'Local family restaurants', 'Food trucks', 'Cook at home more often',
                'Meal prep services', 'Farmer\'s market', 'Community potlucks'
            ],
            'Shopping': [
                'Thrift stores', 'Garage sales', 'Online marketplaces (Facebook, Craigslist)',
                'Outlet malls', 'Seasonal sales', 'Buy second-hand'
            ],
            'Transportation': [
                'Public transit', 'Carpooling', 'Biking or walking',
                'Ride-sharing with friends', 'Fuel-efficient vehicles', 'Plan trips better'
            ],
            'Entertainment': [
                'Free community events', 'Library resources', 'Home movie nights',
                'Outdoor activities', 'Game nights with friends', 'Student discounts'
            ],
            'Health': [
                'Generic medications', 'Preventive care', 'Exercise at home',
                'Community health centers', 'Health insurance optimization', 'Telemedicine'
            ],
            'Utilities': [
                'Energy-efficient appliances', 'LED bulbs', 'Programmable thermostats',
                'Bundle services', 'Compare providers', 'Reduce usage'
            ],
            'Subscriptions': [
                'Cancel unused services', 'Share with family', 'Annual billing discounts',
                'Student rates', 'Free alternatives', 'Rotate services'
            ],
            'Housing': [
                'Roommate arrangements', 'Downsize if possible', 'Energy efficiency upgrades',
                'Rent negotiation', 'Move to lower-cost area', 'House hacking'
            ],
            'Education': [
                'Free online courses', 'Library resources', 'Community college',
                'Scholarships and grants', 'Used textbooks', 'Study groups'
            ],
            'Other': [
                'Compare prices online', 'Wait for sales', 'Buy in bulk',
                'Negotiate prices', 'Use coupons', 'DIY alternatives'
            ]
        }
        
        # Get category-specific alternatives and blend with base alternatives
        specific_alternatives = category_specific.get(category, category_specific['Other'])
        
        # Combine and deduplicate
        combined = []
        seen = set()
        
        # Add category-specific alternatives first (higher priority)
        for alt in specific_alternatives:
            if alt.lower() not in seen:
                combined.append(alt)
                seen.add(alt.lower())
        
        # Add base alternatives that aren't already included
        for alt in base_alternatives:
            if alt.lower() not in seen:
                combined.append(alt)
                seen.add(alt.lower())
        
        return combined[:5]  # Return top 5 alternatives
    
    def _get_category_specific_reasoning(self, base_reasoning: str, category: str) -> str:
        """Generate category-specific reasoning for recommendations"""
        category_contexts = {
            'Dining': f"For {category.lower()} expenses, ",
            'Shopping': f"When shopping for {category.lower()} items, ",
            'Transportation': f"For {category.lower()} needs, ",
            'Entertainment': f"With {category.lower()} spending, ",
            'Health': f"For {category.lower()} expenses, ",
            'Utilities': f"Regarding {category.lower()} costs, ",
            'Subscriptions': f"For {category.lower()} services, ",
            'Housing': f"In {category.lower()} expenses, ",
            'Education': f"For {category.lower()} costs, ",
            'Other': f"For {category.lower()} spending, "
        }
        
        context = category_contexts.get(category, f"For {category.lower()} expenses, ")
        return context + base_reasoning.lower()

    def _get_generic_alternatives(self, category: str) -> List[str]:
        """Get generic alternatives based on category"""
        generic_alternatives = {
            'Restaurants': ['Local restaurants', 'Food trucks', 'Cooking at home', 'Meal prep services', 'Grocery store deli'],
            'Groceries': ['Local grocery stores', 'Farmers markets', 'Bulk buying', 'Online grocery delivery', 'Coupon apps'],
            'Shopping': ['Online retailers', 'Local stores', 'Outlet stores', 'Second-hand shops', 'Price comparison sites'],
            'Transportation': ['Public transit', 'Walking', 'Biking', 'Carpooling', 'Ride-sharing apps'],
            'Entertainment': ['Free activities', 'Library services', 'Streaming at home', 'Local events', 'Group discounts'],
            'Health': ['Generic brands', 'Online pharmacies', 'Local clinics', 'Preventive care', 'Health insurance benefits'],
            'Other': ['Compare prices', 'Look for sales', 'Buy in bulk', 'Use coupons', 'Local alternatives']
        }
        return generic_alternatives.get(category, generic_alternatives['Other'])
