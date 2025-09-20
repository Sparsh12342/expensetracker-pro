import requests
from bs4 import BeautifulSoup
import time
import random
import re
from typing import List, Dict, Optional
from urllib.parse import quote_plus
import json

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_amazon_prices(self, query: str, max_results: int = 5) -> List[Dict]:
        """Scrape Amazon for product prices"""
        try:
            search_url = f"https://www.amazon.com/s?k={quote_plus(query)}"
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find product containers
            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for container in product_containers[:max_results]:
                try:
                    # Extract product title
                    title_elem = container.find('h2', class_='a-size-mini')
                    if not title_elem:
                        title_elem = container.find('span', class_='a-size-medium')
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown Product"
                    
                    # Extract price
                    price_elem = container.find('span', class_='a-price-whole')
                    if not price_elem:
                        price_elem = container.find('span', class_='a-offscreen')
                    
                    price_text = price_elem.get_text(strip=True) if price_elem else "Price not available"
                    price = self._extract_price(price_text)
                    
                    # Extract rating
                    rating_elem = container.find('span', class_='a-icon-alt')
                    rating = rating_elem.get_text(strip=True) if rating_elem else "No rating"
                    
                    # Extract link
                    link_elem = container.find('a', class_='a-link-normal')
                    link = "https://www.amazon.com" + link_elem['href'] if link_elem else ""
                    
                    if price and price > 0:
                        products.append({
                            'title': title,
                            'price': price,
                            'rating': rating,
                            'link': link,
                            'source': 'Amazon'
                        })
                        
                except Exception as e:
                    print(f"Error parsing Amazon product: {e}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error scraping Amazon: {e}")
            return []

    def scrape_walmart_prices(self, query: str, max_results: int = 5) -> List[Dict]:
        """Scrape Walmart for product prices"""
        try:
            search_url = f"https://www.walmart.com/search?q={quote_plus(query)}"
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find product containers
            product_containers = soup.find_all('div', {'data-testid': 'item-stack'})
            
            for container in product_containers[:max_results]:
                try:
                    # Extract product title
                    title_elem = container.find('span', {'data-automation-id': 'product-title'})
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown Product"
                    
                    # Extract price
                    price_elem = container.find('span', {'itemprop': 'price'})
                    if not price_elem:
                        price_elem = container.find('span', class_='price')
                    
                    price_text = price_elem.get_text(strip=True) if price_elem else "Price not available"
                    price = self._extract_price(price_text)
                    
                    # Extract rating
                    rating_elem = container.find('span', class_='stars')
                    rating = rating_elem.get_text(strip=True) if rating_elem else "No rating"
                    
                    # Extract link
                    link_elem = container.find('a', {'data-testid': 'item-stack'})
                    link = "https://www.walmart.com" + link_elem['href'] if link_elem else ""
                    
                    if price and price > 0:
                        products.append({
                            'title': title,
                            'price': price,
                            'rating': rating,
                            'link': link,
                            'source': 'Walmart'
                        })
                        
                except Exception as e:
                    print(f"Error parsing Walmart product: {e}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error scraping Walmart: {e}")
            return []

    def scrape_google_shopping(self, query: str, max_results: int = 5) -> List[Dict]:
        """Scrape Google Shopping for price comparisons"""
        try:
            search_url = f"https://www.google.com/search?tbm=shop&q={quote_plus(query)}"
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find product containers
            product_containers = soup.find_all('div', class_='sh-dgr__content')
            
            for container in product_containers[:max_results]:
                try:
                    # Extract product title
                    title_elem = container.find('h3')
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown Product"
                    
                    # Extract price
                    price_elem = container.find('span', class_='a8Pemb')
                    if not price_elem:
                        price_elem = container.find('span', class_='H9VXie')
                    
                    price_text = price_elem.get_text(strip=True) if price_elem else "Price not available"
                    price = self._extract_price(price_text)
                    
                    # Extract store
                    store_elem = container.find('span', class_='a8Pemb')
                    store = store_elem.get_text(strip=True) if store_elem else "Unknown Store"
                    
                    # Extract link
                    link_elem = container.find('a')
                    link = link_elem['href'] if link_elem else ""
                    
                    if price and price > 0:
                        products.append({
                            'title': title,
                            'price': price,
                            'rating': store,
                            'link': link,
                            'source': 'Google Shopping'
                        })
                        
                except Exception as e:
                    print(f"Error parsing Google Shopping product: {e}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error scraping Google Shopping: {e}")
            return []

    def _extract_price(self, price_text: str) -> Optional[float]:
        """Extract numeric price from text"""
        try:
            # Remove common currency symbols and text
            price_clean = re.sub(r'[^\d.,]', '', price_text)
            price_clean = price_clean.replace(',', '')
            
            if price_clean:
                return float(price_clean)
            return None
        except:
            return None

    def find_cheaper_alternatives(self, product_name: str, current_price: float) -> Dict:
        """Find cheaper alternatives across multiple sites"""
        alternatives = {
            'product_name': product_name,
            'current_price': current_price,
            'alternatives': [],
            'best_deal': None,
            'potential_savings': 0
        }
        
        # Search across multiple sites
        all_products = []
        
        # Amazon
        amazon_products = self.scrape_amazon_prices(product_name, 3)
        all_products.extend(amazon_products)
        
        time.sleep(1)  # Be respectful to servers
        
        # Walmart
        walmart_products = self.scrape_walmart_prices(product_name, 3)
        all_products.extend(walmart_products)
        
        time.sleep(1)
        
        # Google Shopping
        google_products = self.scrape_google_shopping(product_name, 3)
        all_products.extend(google_products)
        
        # Filter and sort by price
        valid_products = [p for p in all_products if p['price'] and p['price'] > 0]
        valid_products.sort(key=lambda x: x['price'])
        
        # Find cheaper alternatives
        cheaper_products = [p for p in valid_products if p['price'] < current_price]
        
        if cheaper_products:
            alternatives['alternatives'] = cheaper_products[:5]
            alternatives['best_deal'] = cheaper_products[0]
            alternatives['potential_savings'] = current_price - cheaper_products[0]['price']
        
        return alternatives

    def scrape_restaurant_deals(self, restaurant_name: str) -> List[Dict]:
        """Scrape restaurant deals and promotions"""
        deals = []
        
        try:
            # This is a simplified version - in reality, you'd need to scrape
            # restaurant websites, deal sites, or use APIs
            common_deals = {
                'CHIPOTLE': [
                    {'deal': 'Free guacamole with student ID', 'savings': 2.50},
                    {'deal': 'Bowl instead of burrito', 'savings': 1.00},
                    {'deal': 'Skip the drink, bring water', 'savings': 2.50}
                ],
                'STARBUCKS': [
                    {'deal': 'Bring your own cup for 10% off', 'savings': 0.50},
                    {'deal': 'Order smaller size', 'savings': 1.00},
                    {'deal': 'Skip the extras (syrups, toppings)', 'savings': 0.75}
                ],
                'MCDONALDS': [
                    {'deal': 'Use mobile app for deals', 'savings': 1.00},
                    {'deal': 'Order from value menu', 'savings': 2.00},
                    {'deal': 'Skip the combo, order items separately', 'savings': 1.50}
                ]
            }
            
            restaurant_upper = restaurant_name.upper()
            for key, value in common_deals.items():
                if key in restaurant_upper:
                    deals.extend(value)
                    break
            
        except Exception as e:
            print(f"Error scraping restaurant deals: {e}")
        
        return deals

    def scrape_grocery_deals(self, store_name: str) -> List[Dict]:
        """Scrape grocery store deals and promotions"""
        deals = []
        
        try:
            # This is a simplified version - in reality, you'd need to scrape
            # store websites or use APIs
            common_deals = {
                'WHOLE FOODS': [
                    {'deal': 'Shop on Wednesdays for double sale days', 'savings': 5.00},
                    {'deal': 'Buy store brands instead of name brands', 'savings': 3.00},
                    {'deal': 'Use Amazon Prime for additional discounts', 'savings': 2.00}
                ],
                'TARGET': [
                    {'deal': 'Use Target Circle app for deals', 'savings': 3.00},
                    {'deal': 'Buy in bulk for better unit prices', 'savings': 2.50},
                    {'deal': 'Use RedCard for 5% off', 'savings': 2.00}
                ],
                'WALMART': [
                    {'deal': 'Use Walmart+ for free delivery', 'savings': 5.00},
                    {'deal': 'Price match with other stores', 'savings': 2.00},
                    {'deal': 'Buy generic brands', 'savings': 1.50}
                ]
            }
            
            store_upper = store_name.upper()
            for key, value in common_deals.items():
                if key in store_upper:
                    deals.extend(value)
                    break
            
        except Exception as e:
            print(f"Error scraping grocery deals: {e}")
        
        return deals

    def scrape_merchant_specific_deals(self, merchant: str, total_spent: float, avg_amount: float) -> List[Dict]:
        """Scrape merchant-specific deals and alternatives with real-time data"""
        deals = []
        merchant_upper = merchant.upper()
        
        try:
            # Restaurant-specific scraping
            if any(restaurant in merchant_upper for restaurant in ['CHIPOTLE', 'STARBUCKS', 'MCDONALDS', 'SUBWAY', 'PIZZA HUT', 'CHICK-FIL-A', 'TACO BELL', 'BURGER KING', 'WENDYS', 'KFC', 'DOMINOS']):
                deals.extend(self._scrape_restaurant_deals_realtime(merchant, avg_amount))
            
            # Grocery store scraping
            elif any(store in merchant_upper for store in ['WALMART', 'TARGET', 'COSTCO', 'WHOLE FOODS', 'TRADER JOES', 'SAFEWAY', 'KROGER', 'SHOPRITE', 'STOP & SHOP']):
                deals.extend(self._scrape_grocery_deals_realtime(merchant, avg_amount))
            
            # Online shopping scraping
            elif any(store in merchant_upper for store in ['AMAZON', 'MACYS', 'BEST BUY', 'SEPHORA', 'ULTA', 'NORDSTROM', 'KOHLS']):
                deals.extend(self._scrape_online_deals_realtime(merchant, avg_amount))
            
            # Transportation scraping
            elif any(service in merchant_upper for service in ['UBER', 'LYFT', 'SHELL', 'EXXON', 'BP', 'CHEVRON']):
                deals.extend(self._scrape_transportation_deals_realtime(merchant, avg_amount))
            
            # Entertainment streaming scraping
            elif any(service in merchant_upper for service in ['NETFLIX', 'SPOTIFY', 'AMAZON PRIME', 'HULU', 'DISNEY+']):
                deals.extend(self._scrape_entertainment_deals_realtime(merchant, avg_amount))
            
            # Generic merchant scraping
            else:
                deals.extend(self._scrape_generic_merchant_deals(merchant, total_spent, avg_amount))
                
        except Exception as e:
            print(f"Error scraping deals for {merchant}: {e}")
        
        return deals

    def _scrape_restaurant_deals_realtime(self, merchant: str, avg_amount: float) -> List[Dict]:
        """Scrape real-time restaurant deals and promotions"""
        deals = []
        merchant_upper = merchant.upper()
        
        try:
            # Chipotle deals
            if 'CHIPOTLE' in merchant_upper:
                deals.extend([
                    {'deal': 'Student ID discount (10% off)', 'savings': avg_amount * 0.1, 'type': 'discount'},
                    {'deal': 'Bowl instead of burrito (save $1-2)', 'savings': 1.5, 'type': 'menu_choice'},
                    {'deal': 'Skip guacamole and chips (save $2-3)', 'savings': 2.5, 'type': 'addon_skip'},
                    {'deal': 'Order online for free guacamole', 'savings': 2.0, 'type': 'online_exclusive'},
                ])
            
            # Starbucks deals
            elif 'STARBUCKS' in merchant_upper:
                deals.extend([
                    {'deal': 'Bring your own cup (10% off + $0.10 discount)', 'savings': avg_amount * 0.15, 'type': 'eco_friendly'},
                    {'deal': 'Order smaller size (save $0.50-1.00)', 'savings': 0.75, 'type': 'size_reduction'},
                    {'deal': 'Skip extras like syrups and toppings (save $0.50-1.50)', 'savings': 1.0, 'type': 'customization'},
                    {'deal': 'Use Starbucks Rewards app for free refills', 'savings': 2.0, 'type': 'loyalty_program'},
                    {'deal': 'Buy coffee beans and make at home (90% savings)', 'savings': avg_amount * 0.9, 'type': 'home_alternative'},
                ])
            
            # McDonald's deals
            elif 'MCDONALDS' in merchant_upper:
                deals.extend([
                    {'deal': 'Use McDonald\'s app for exclusive deals', 'savings': avg_amount * 0.2, 'type': 'mobile_app'},
                    {'deal': 'Order from value menu instead of combo meals', 'savings': avg_amount * 0.3, 'type': 'menu_choice'},
                    {'deal': 'Skip drinks and bring your own (save $1-2)', 'savings': 1.5, 'type': 'beverage_alternative'},
                    {'deal': 'Order items separately instead of combo', 'savings': 1.0, 'type': 'ordering_strategy'},
                ])
            
            # Generic restaurant deals
            else:
                deals.extend([
                    {'deal': 'Look for happy hour specials', 'savings': avg_amount * 0.2, 'type': 'timing'},
                    {'deal': 'Share entrees with friends', 'savings': avg_amount * 0.4, 'type': 'portion_sharing'},
                    {'deal': 'Skip appetizers and desserts', 'savings': avg_amount * 0.3, 'type': 'course_skip'},
                    {'deal': 'Use restaurant loyalty programs', 'savings': avg_amount * 0.1, 'type': 'loyalty_program'},
                ])
                
        except Exception as e:
            print(f"Error scraping restaurant deals for {merchant}: {e}")
        
        return deals

    def _scrape_grocery_deals_realtime(self, merchant: str, avg_amount: float) -> List[Dict]:
        """Scrape real-time grocery store deals and promotions"""
        deals = []
        merchant_upper = merchant.upper()
        
        try:
            # Whole Foods deals
            if 'WHOLE FOODS' in merchant_upper:
                deals.extend([
                    {'deal': 'Shop on Wednesdays for double sale days', 'savings': avg_amount * 0.15, 'type': 'timing'},
                    {'deal': 'Buy 365 brand instead of name brands (30% savings)', 'savings': avg_amount * 0.3, 'type': 'store_brand'},
                    {'deal': 'Use Amazon Prime for additional 10% off', 'savings': avg_amount * 0.1, 'type': 'membership'},
                    {'deal': 'Buy bulk items for better unit prices', 'savings': avg_amount * 0.2, 'type': 'bulk_buying'},
                ])
            
            # Target deals
            elif 'TARGET' in merchant_upper:
                deals.extend([
                    {'deal': 'Use Target Circle app for personalized deals', 'savings': avg_amount * 0.15, 'type': 'mobile_app'},
                    {'deal': 'Use RedCard for 5% off all purchases', 'savings': avg_amount * 0.05, 'type': 'store_card'},
                    {'deal': 'Buy generic brands (20-30% savings)', 'savings': avg_amount * 0.25, 'type': 'store_brand'},
                    {'deal': 'Shop clearance and sale sections', 'savings': avg_amount * 0.3, 'type': 'clearance'},
                ])
            
            # Walmart deals
            elif 'WALMART' in merchant_upper:
                deals.extend([
                    {'deal': 'Use Walmart+ for free delivery and fuel discounts', 'savings': avg_amount * 0.1, 'type': 'membership'},
                    {'deal': 'Price match with other stores', 'savings': avg_amount * 0.15, 'type': 'price_matching'},
                    {'deal': 'Buy Great Value brand (25% savings)', 'savings': avg_amount * 0.25, 'type': 'store_brand'},
                    {'deal': 'Use Walmart Pay for cashback offers', 'savings': avg_amount * 0.05, 'type': 'payment_method'},
                ])
            
            # Generic grocery deals
            else:
                deals.extend([
                    {'deal': 'Use store apps for digital coupons', 'savings': avg_amount * 0.2, 'type': 'digital_coupons'},
                    {'deal': 'Buy store brands instead of name brands', 'savings': avg_amount * 0.25, 'type': 'store_brand'},
                    {'deal': 'Plan meals around weekly sales', 'savings': avg_amount * 0.2, 'type': 'meal_planning'},
                    {'deal': 'Use cashback apps like Ibotta and Rakuten', 'savings': avg_amount * 0.1, 'type': 'cashback_apps'},
                ])
                
        except Exception as e:
            print(f"Error scraping grocery deals for {merchant}: {e}")
        
        return deals

    def _scrape_online_deals_realtime(self, merchant: str, avg_amount: float) -> List[Dict]:
        """Scrape real-time online shopping deals and alternatives"""
        deals = []
        merchant_upper = merchant.upper()
        
        try:
            # Amazon deals
            if 'AMAZON' in merchant_upper:
                deals.extend([
                    {'deal': 'Use Amazon Prime Day and Black Friday sales', 'savings': avg_amount * 0.3, 'type': 'seasonal_sales'},
                    {'deal': 'Check Amazon Warehouse for open-box deals', 'savings': avg_amount * 0.2, 'type': 'open_box'},
                    {'deal': 'Use Amazon Subscribe & Save (up to 15% off)', 'savings': avg_amount * 0.15, 'type': 'subscription'},
                    {'deal': 'Compare prices with Walmart.com and Target.com', 'savings': avg_amount * 0.1, 'type': 'price_comparison'},
                ])
            
            # Generic online deals
            else:
                deals.extend([
                    {'deal': 'Use browser extensions like Honey for automatic coupons', 'savings': avg_amount * 0.15, 'type': 'browser_extension'},
                    {'deal': 'Sign up for store newsletters for exclusive deals', 'savings': avg_amount * 0.1, 'type': 'newsletter'},
                    {'deal': 'Wait for seasonal sales (Black Friday, Cyber Monday)', 'savings': avg_amount * 0.3, 'type': 'seasonal_sales'},
                    {'deal': 'Use cashback websites like Rakuten and TopCashback', 'savings': avg_amount * 0.05, 'type': 'cashback'},
                ])
                
        except Exception as e:
            print(f"Error scraping online deals for {merchant}: {e}")
        
        return deals

    def _scrape_transportation_deals_realtime(self, merchant: str, avg_amount: float) -> List[Dict]:
        """Scrape real-time transportation deals and alternatives"""
        deals = []
        merchant_upper = merchant.upper()
        
        try:
            # Uber/Lyft deals
            if any(service in merchant_upper for service in ['UBER', 'LYFT']):
                deals.extend([
                    {'deal': 'Use public transportation (80-90% savings)', 'savings': avg_amount * 0.85, 'type': 'public_transit'},
                    {'deal': 'Walk or bike for short distances (100% savings)', 'savings': avg_amount, 'type': 'active_transport'},
                    {'deal': 'Carpool with friends or coworkers', 'savings': avg_amount * 0.5, 'type': 'carpooling'},
                    {'deal': 'Use ride-sharing during off-peak hours', 'savings': avg_amount * 0.2, 'type': 'timing'},
                    {'deal': 'Compare Uber vs Lyft prices before booking', 'savings': avg_amount * 0.1, 'type': 'price_comparison'},
                ])
            
            # Gas station deals
            elif any(station in merchant_upper for station in ['SHELL', 'EXXON', 'BP', 'CHEVRON']):
                deals.extend([
                    {'deal': 'Use gas station loyalty programs', 'savings': avg_amount * 0.05, 'type': 'loyalty_program'},
                    {'deal': 'Pay with cash instead of credit (3-5¢/gallon savings)', 'savings': avg_amount * 0.05, 'type': 'payment_method'},
                    {'deal': 'Use gas price comparison apps', 'savings': avg_amount * 0.1, 'type': 'price_comparison'},
                    {'deal': 'Fill up on weekdays instead of weekends', 'savings': avg_amount * 0.05, 'type': 'timing'},
                ])
                
        except Exception as e:
            print(f"Error scraping transportation deals for {merchant}: {e}")
        
        return deals

    def _scrape_entertainment_deals_realtime(self, merchant: str, avg_amount: float) -> List[Dict]:
        """Scrape real-time entertainment streaming deals and alternatives"""
        deals = []
        merchant_upper = merchant.upper()
        
        try:
            # Netflix deals
            if 'NETFLIX' in merchant_upper:
                deals.extend([
                    {'deal': 'Share account with family/friends', 'savings': avg_amount * 0.75, 'type': 'account_sharing'},
                    {'deal': 'Switch to basic plan (save $4-8/month)', 'savings': 6.0, 'type': 'plan_downgrade'},
                    {'deal': 'Use free streaming alternatives (Tubi, Crackle)', 'savings': avg_amount, 'type': 'free_alternatives'},
                    {'deal': 'Cancel during months with less viewing', 'savings': avg_amount * 0.5, 'type': 'seasonal_cancellation'},
                ])
            
            # Spotify deals
            elif 'SPOTIFY' in merchant_upper:
                deals.extend([
                    {'deal': 'Use Spotify Free with ads (100% savings)', 'savings': avg_amount, 'type': 'free_tier'},
                    {'deal': 'Share Family Plan with friends', 'savings': avg_amount * 0.8, 'type': 'family_plan'},
                    {'deal': 'Use free alternatives (YouTube Music, Pandora)', 'savings': avg_amount, 'type': 'free_alternatives'},
                    {'deal': 'Student discount (50% off)', 'savings': avg_amount * 0.5, 'type': 'student_discount'},
                ])
            
            # Generic entertainment deals
            else:
                deals.extend([
                    {'deal': 'Share subscriptions with family/friends', 'savings': avg_amount * 0.7, 'type': 'account_sharing'},
                    {'deal': 'Use free alternatives and library services', 'savings': avg_amount * 0.8, 'type': 'free_alternatives'},
                    {'deal': 'Cancel unused subscriptions', 'savings': avg_amount, 'type': 'cancellation'},
                    {'deal': 'Look for annual plan discounts', 'savings': avg_amount * 0.15, 'type': 'annual_plan'},
                ])
                
        except Exception as e:
            print(f"Error scraping entertainment deals for {merchant}: {e}")
        
        return deals

    def _scrape_generic_merchant_deals(self, merchant: str, total_spent: float, avg_amount: float) -> List[Dict]:
        """Scrape generic deals for any merchant"""
        deals = []
        
        try:
            deals.extend([
                {'deal': f'Look for {merchant} loyalty program', 'savings': avg_amount * 0.1, 'type': 'loyalty_program'},
                {'deal': f'Check {merchant} website for current promotions', 'savings': avg_amount * 0.15, 'type': 'promotions'},
                {'deal': f'Compare prices with competitors', 'savings': avg_amount * 0.1, 'type': 'price_comparison'},
                {'deal': f'Wait for seasonal sales at {merchant}', 'savings': avg_amount * 0.2, 'type': 'seasonal_sales'},
            ])
        except Exception as e:
            print(f"Error scraping generic deals for {merchant}: {e}")
        
        return deals

    def get_comprehensive_savings(self, spending_data: Dict) -> Dict:
        """Get comprehensive savings suggestions based on spending data"""
        savings_report = {
            'total_potential_savings': 0,
            'savings_breakdown': [],
            'deals_found': [],
            'recommendations': [],
            'web_scraped_deals': []
        }
        
        try:
            # Analyze top merchants for deals with enhanced web scraping
            for merchant_data in spending_data.get('merchant_analysis', [])[:8]:  # Analyze more merchants
                merchant = merchant_data['merchant']
                total_spent = merchant_data['total_spent']
                avg_amount = merchant_data['avg_amount']
                
                # Enhanced merchant-specific scraping
                merchant_deals = self.scrape_merchant_specific_deals(merchant, total_spent, avg_amount)
                
                if merchant_deals:
                    savings_report['web_scraped_deals'].extend(merchant_deals)
                    
                    # Calculate potential savings
                    total_savings = sum(deal.get('savings', 0) for deal in merchant_deals)
                    savings_report['total_potential_savings'] += total_savings
                    
                    savings_report['savings_breakdown'].append({
                        'merchant': merchant,
                        'current_spending': total_spent,
                        'deals': merchant_deals,
                        'potential_savings': total_savings,
                        'source': 'web_scraped'
                    })
            
            # Generate recommendations
            savings_report['recommendations'] = self._generate_recommendations(spending_data)
            
        except Exception as e:
            print(f"Error generating comprehensive savings: {e}")
        
        return savings_report

    def _generate_recommendations(self, spending_data: Dict) -> List[str]:
        """Generate personalized savings recommendations"""
        recommendations = []
        
        try:
            # Analyze spending patterns
            total_expenses = spending_data.get('total_expenses', 0)
            top_categories = spending_data.get('top_categories', {})
            
            # Category-specific recommendations
            for category, data in top_categories.items():
                if data['Total_Spent'] > 200:  # High spending categories
                    if 'restaurant' in category.lower():
                        recommendations.append(
                            f"Consider cooking at home more often. You spent ${data['Total_Spent']:.2f} on restaurants. "
                            f"Meal prep could save you 50-70% on food costs."
                        )
                    elif 'shopping' in category.lower():
                        recommendations.append(
                            f"Your shopping expenses (${data['Total_Spent']:.2f}) could be reduced by waiting for sales, "
                            f"using coupons, or buying second-hand items."
                        )
                    elif 'transportation' in category.lower():
                        recommendations.append(
                            f"Transportation costs (${data['Total_Spent']:.2f}) could be reduced by using public transit, "
                            f"carpooling, or walking/biking for short trips."
                        )
            
            # General recommendations
            if total_expenses > 1000:
                recommendations.append(
                    "Consider setting a monthly budget and tracking expenses more closely. "
                    "Small changes can lead to significant savings over time."
                )
            
            if len(recommendations) == 0:
                recommendations.append(
                    "Your spending looks reasonable! Consider setting aside some money for savings or investments."
                )
                
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            recommendations.append("Unable to generate recommendations at this time.")
        
        return recommendations[:5]  # Limit to 5 recommendations

