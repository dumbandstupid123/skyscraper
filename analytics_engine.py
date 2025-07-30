import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import statistics
import math

class AnalyticsEngine:
    """Advanced analytics engine for client risk assessment and resource tracking."""
    
    def __init__(self):
        self.clients_file = 'clients.json'
        self.resources_file = 'structured_resources.json'
    
    def load_clients(self) -> Dict[str, Any]:
        """Load clients data from JSON file."""
        try:
            if os.path.exists(self.clients_file):
                with open(self.clients_file, 'r') as f:
                    return json.load(f)
            return {'clients': []}
        except Exception as e:
            print(f"Error loading clients: {e}")
            return {'clients': []}
    
    def load_resources(self) -> List[Dict[str, Any]]:
        """Load resources data from JSON file."""
        try:
            if os.path.exists(self.resources_file):
                with open(self.resources_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading resources: {e}")
            return []
    
    def calculate_risk_assessment_percentage(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive risk assessment percentage for a client.
        Returns risk score (0-100) with detailed breakdown.
        """
        risk_factors = {}
        total_score = 0
        max_possible_score = 0
        
        # 1. Housing Stability Risk (25 points max)
        housing_risk = self._assess_housing_risk(client)
        risk_factors['housing'] = housing_risk
        total_score += housing_risk['score']
        max_possible_score += housing_risk['max_score']
        
        # 2. Financial Risk (20 points max)
        financial_risk = self._assess_financial_risk(client)
        risk_factors['financial'] = financial_risk
        total_score += financial_risk['score']
        max_possible_score += financial_risk['max_score']
        
        # 3. Health & Safety Risk (20 points max)
        health_risk = self._assess_health_safety_risk(client)
        risk_factors['health_safety'] = health_risk
        total_score += health_risk['score']
        max_possible_score += health_risk['max_score']
        
        # 4. Social Support Risk (15 points max)
        social_risk = self._assess_social_support_risk(client)
        risk_factors['social_support'] = social_risk
        total_score += social_risk['score']
        max_possible_score += social_risk['max_score']
        
        # 5. Family/Children Risk (10 points max)
        family_risk = self._assess_family_risk(client)
        risk_factors['family'] = family_risk
        total_score += family_risk['score']
        max_possible_score += family_risk['max_score']
        
        # 6. Employment/Income Risk (10 points max)
        employment_risk = self._assess_employment_risk(client)
        risk_factors['employment'] = employment_risk
        total_score += employment_risk['score']
        max_possible_score += employment_risk['max_score']
        
        # Calculate final percentage
        risk_percentage = (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0
        
        # Determine risk level
        if risk_percentage >= 80:
            risk_level = "CRITICAL"
        elif risk_percentage >= 60:
            risk_level = "HIGH"
        elif risk_percentage >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            'client_id': client.get('id'),
            'risk_percentage': round(risk_percentage, 1),
            'risk_level': risk_level,
            'total_score': total_score,
            'max_possible_score': max_possible_score,
            'risk_factors': risk_factors,
            'recommendations': self._generate_risk_recommendations(risk_factors, risk_percentage),
            'last_calculated': datetime.now().isoformat()
        }
    
    def _assess_housing_risk(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """Assess housing-related risk factors."""
        score = 0
        max_score = 25
        details = []
        
        # Check housing situation from different data sources
        housing_status = None
        worried_about_housing = None
        
        # Check intake submission data
        if client.get('source') == 'patient_intake_app':
            family_housing = client.get('familyAndHousing', {})
            housing_status = family_housing.get('housingSituation', '')
            worried_about_housing = family_housing.get('worriedAboutHousing', '')
        
        # Check regular client data
        if not housing_status:
            housing_status = client.get('housing_status', client.get('family_status', ''))
        
        # Score based on housing status
        if housing_status:
            if 'homeless' in housing_status.lower():
                if 'sleeping outside' in housing_status.lower():
                    score += 25  # Highest risk
                    details.append("Currently homeless (sleeping outside)")
                else:
                    score += 20  # High risk but in shelter
                    details.append("Currently homeless (in shelter)")
            elif 'evicted' in housing_status.lower():
                score += 18
                details.append("Recently evicted")
            elif 'behind on rent' in housing_status.lower():
                score += 15
                details.append("Behind on rent/mortgage")
            elif 'staying with friends' in housing_status.lower() or 'temporarily' in housing_status.lower():
                score += 12
                details.append("Temporary housing arrangement")
            elif 'overcrowded' in housing_status.lower():
                score += 10
                details.append("Living in overcrowded conditions")
            elif 'transitional' in housing_status.lower():
                score += 8
                details.append("In transitional housing")
            elif 'subsidized' in housing_status.lower():
                score += 5
                details.append("In subsidized housing")
        
        # Additional points for housing worry
        if worried_about_housing and worried_about_housing.lower() == 'yes':
            score += 5
            details.append("Worried about housing stability")
        
        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'details': details,
            'housing_status': housing_status
        }
    
    def _assess_financial_risk(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """Assess financial risk factors."""
        score = 0
        max_score = 20
        details = []
        
        # Check income from different sources
        income = None
        work_status = None
        
        if client.get('source') == 'patient_intake_app':
            money_resources = client.get('moneyAndResources', {})
            income = money_resources.get('annualIncome', '')
            work_status = money_resources.get('workSituation', '')
        else:
            income = client.get('income_level', 0)
            work_status = client.get('employment_status', '')
        
        # Score based on income
        if isinstance(income, str):
            if income in ['$0', 'Under $10,000']:
                score += 15
                details.append("Extremely low income (under $10,000)")
            elif income in ['$10,000-$15,000']:
                score += 12
                details.append("Very low income ($10,000-$15,000)")
            elif income in ['$15,000-$25,000']:
                score += 8
                details.append("Low income ($15,000-$25,000)")
            elif income in ['$25,000-$35,000']:
                score += 5
                details.append("Below median income")
        elif isinstance(income, (int, float)):
            if income < 10000:
                score += 15
                details.append(f"Extremely low income (${income:,})")
            elif income < 15000:
                score += 12
                details.append(f"Very low income (${income:,})")
            elif income < 25000:
                score += 8
                details.append(f"Low income (${income:,})")
        
        # Score based on employment status
        if work_status:
            if work_status.lower() == 'unemployed':
                score += 5
                details.append("Currently unemployed")
            elif 'part-time' in work_status.lower():
                score += 3
                details.append("Part-time employment")
            elif 'disabled' in work_status.lower():
                score += 4
                details.append("Unable to work due to disability")
        
        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'details': details,
            'income': income,
            'work_status': work_status
        }
    
    def _assess_health_safety_risk(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """Assess health and safety risk factors."""
        score = 0
        max_score = 20
        details = []
        
        # Check for safety concerns
        if client.get('source') == 'patient_intake_app':
            safety = client.get('safetyQuestions', {})
            basic_needs = client.get('basicNeeds', {})
            unable_to_get = basic_needs.get('unableToGet', {})
            stress_level = basic_needs.get('stressLevel', '')
            
            # Violence/safety concerns
            if safety.get('experiencingViolence') == 'Yes':
                score += 10
                details.append("Experiencing violence")
            
            if safety.get('safePlace') == 'No':
                score += 8
                details.append("No safe place to go")
            
            if safety.get('needsImmediateHelp'):
                score += 6
                details.append("Needs immediate help")
            
            # Health access issues
            if unable_to_get and unable_to_get.get('medicine'):
                score += 5
                details.append("Unable to access medicine")
            
            # Stress level
            if stress_level == 'Very High':
                score += 4
                details.append("Very high stress level")
            elif stress_level == 'High':
                score += 2
                details.append("High stress level")
        
        # Check existing client needs
        needs = client.get('needs', [])
        if isinstance(needs, list):
            for need in needs:
                if 'domestic violence' in need.lower():
                    score += 8
                    details.append("Domestic violence support needed")
                elif 'mental health' in need.lower():
                    score += 4
                    details.append("Mental health support needed")
                elif 'substance abuse' in need.lower():
                    score += 4
                    details.append("Substance abuse treatment needed")
        
        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'details': details
        }
    
    def _assess_social_support_risk(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """Assess social support risk factors."""
        score = 0
        max_score = 15
        details = []
        
        if client.get('source') == 'patient_intake_app':
            basic_needs = client.get('basicNeeds', {})
            social_contact = basic_needs.get('socialContact', '')
            
            if social_contact == 'Never':
                score += 10
                details.append("No social contact")
            elif social_contact == 'Rarely':
                score += 7
                details.append("Rarely has social contact")
            elif social_contact == 'Sometimes':
                score += 3
                details.append("Limited social contact")
        
        # Check family status
        family_status = client.get('family_status', '')
        if 'single' in family_status.lower():
            score += 2
            details.append("Single/limited family support")
        
        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'details': details
        }
    
    def _assess_family_risk(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """Assess family and children risk factors."""
        score = 0
        max_score = 10
        details = []
        
        # Check for children
        family_members = None
        if client.get('source') == 'patient_intake_app':
            family_housing = client.get('familyAndHousing', {})
            family_members = family_housing.get('familyMembers', '')
        
        if family_members and 'children' in family_members.lower():
            score += 3
            details.append("Has children")
            
            # Additional risk if single parent
            if 'single parent' in family_members.lower():
                score += 2
                details.append("Single parent")
        
        # Check for child welfare needs
        needs = client.get('needs', [])
        if isinstance(needs, list):
            for need in needs:
                if 'child' in need.lower() or 'childcare' in need.lower():
                    score += 3
                    details.append("Child welfare concerns")
                    break
        
        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'details': details
        }
    
    def _assess_employment_risk(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """Assess employment-related risk factors."""
        score = 0
        max_score = 10
        details = []
        
        # This overlaps with financial but focuses on employment stability
        work_status = None
        education = None
        
        if client.get('source') == 'patient_intake_app':
            money_resources = client.get('moneyAndResources', {})
            work_status = money_resources.get('workSituation', '')
            education = money_resources.get('educationLevel', '')
        else:
            work_status = client.get('employment_status', '')
        
        if work_status:
            if work_status.lower() == 'unemployed':
                score += 6
                details.append("Currently unemployed")
            elif 'looking for work' in work_status.lower():
                score += 4
                details.append("Actively seeking employment")
            elif 'seasonal' in work_status.lower():
                score += 3
                details.append("Seasonal/unstable employment")
        
        # Education level impact
        if education:
            if education in ['No formal education', 'Less than high school']:
                score += 2
                details.append("Limited education")
        
        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'details': details
        }
    
    def _generate_risk_recommendations(self, risk_factors: Dict[str, Any], risk_percentage: float) -> List[str]:
        """Generate recommendations based on risk assessment."""
        recommendations = []
        
        # Housing recommendations
        housing = risk_factors.get('housing', {})
        if housing.get('score', 0) > 15:
            recommendations.append("URGENT: Housing intervention required")
        elif housing.get('score', 0) > 10:
            recommendations.append("Housing assistance should be prioritized")
        
        # Financial recommendations
        financial = risk_factors.get('financial', {})
        if financial.get('score', 0) > 12:
            recommendations.append("Emergency financial assistance needed")
        elif financial.get('score', 0) > 8:
            recommendations.append("Financial counseling and support recommended")
        
        # Health/Safety recommendations
        health = risk_factors.get('health_safety', {})
        if health.get('score', 0) > 10:
            recommendations.append("URGENT: Safety assessment and intervention required")
        elif health.get('score', 0) > 5:
            recommendations.append("Health and safety support recommended")
        
        # Overall risk recommendations
        if risk_percentage >= 80:
            recommendations.append("CRITICAL: Immediate comprehensive intervention required")
        elif risk_percentage >= 60:
            recommendations.append("High priority case - weekly check-ins recommended")
        
        return recommendations
    
    def get_resource_usage_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get resource usage trends over the specified number of days."""
        clients_data = self.load_clients()
        
        # Create date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Track resource usage by day and category
        daily_usage = defaultdict(lambda: defaultdict(int))
        category_trends = defaultdict(list)
        status_distribution = defaultdict(int)
        
        for client in clients_data.get('clients', []):
            if 'resources' in client:
                for resource in client['resources']:
                    added_date_str = resource.get('added_date', '')
                    if added_date_str:
                        try:
                            added_date = datetime.fromisoformat(added_date_str.replace('Z', '+00:00'))
                            if start_date <= added_date <= end_date:
                                day_key = added_date.strftime('%Y-%m-%d')
                                category = resource.get('category', 'other')
                                
                                daily_usage[day_key][category] += 1
                                daily_usage[day_key]['total'] += 1
                                
                                # Track status distribution
                                status = resource.get('status', 'pending')
                                status_distribution[status] += 1
                        except:
                            continue
        
        # Generate trend data
        trend_data = []
        categories = set()
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            day_key = current_date.strftime('%Y-%m-%d')
            day_data = daily_usage.get(day_key, {})
            
            trend_point = {
                'date': day_key,
                'total': day_data.get('total', 0)
            }
            
            # Add category breakdown
            for category in ['housing', 'food', 'transportation', 'mental_health_substance_abuse', 'immigration_legal', 'goods_clothing', 'utilities', 'other']:
                count = day_data.get(category, 0)
                trend_point[category] = count
                if count > 0:
                    categories.add(category)
        
            trend_data.append(trend_point)
        
        return {
            'period_days': days,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'trend_data': trend_data,
            'categories_used': list(categories),
            'status_distribution': dict(status_distribution),
            'total_resources_accessed': sum(day.get('total', 0) for day in daily_usage.values())
        }
    
    def get_comprehensive_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive statistical breakdown of all data."""
        clients_data = self.load_clients()
        resources_data = self.load_resources()
        clients = clients_data.get('clients', [])
        
        # Calculate risk assessments for all clients
        risk_assessments = []
        for client in clients:
            risk_assessment = self.calculate_risk_assessment_percentage(client)
            risk_assessments.append(risk_assessment)
        
        # Basic statistics
        total_clients = len(clients)
        intake_submissions = [c for c in clients if c.get('source') == 'patient_intake_app']
        regular_clients = [c for c in clients if c.get('source') != 'patient_intake_app']
        
        # Demographics analysis
        demographics = self._analyze_demographics(clients)
        
        # Risk analysis
        risk_analysis = self._analyze_risk_distribution(risk_assessments)
        
        # Resource analysis
        resource_analysis = self._analyze_resource_usage(clients)
        
        # Needs analysis
        needs_analysis = self._analyze_client_needs(clients)
        
        # Geographic analysis
        geographic_analysis = self._analyze_geographic_distribution(clients)
        
        # Outcome tracking
        outcome_analysis = self._analyze_outcomes(clients)
        
        return {
            'last_updated': datetime.now().isoformat(),
            'overview': {
                'total_clients': total_clients,
                'intake_submissions': len(intake_submissions),
                'active_clients': len(regular_clients),
                'total_resources_available': len(resources_data),
                'total_resources_assigned': sum(len(c.get('resources', [])) for c in clients)
            },
            'demographics': demographics,
            'risk_analysis': risk_analysis,
            'resource_analysis': resource_analysis,
            'needs_analysis': needs_analysis,
            'geographic_analysis': geographic_analysis,
            'outcome_analysis': outcome_analysis,
            'detailed_risk_assessments': risk_assessments
        }
    
    def _analyze_demographics(self, clients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze demographic distribution."""
        demographics = {
            'gender': defaultdict(int),
            'age_groups': defaultdict(int),
            'family_status': defaultdict(int),
            'employment_status': defaultdict(int),
            'veteran_status': defaultdict(int),
            'language': defaultdict(int),
            'race_ethnicity': defaultdict(int)
        }
        
        for client in clients:
            # Gender
            gender = client.get('gender', 'Unknown')
            demographics['gender'][gender] += 1
            
            # Age groups
            age = self._calculate_age(client.get('dateOfBirth', ''))
            if age:
                if age < 18:
                    demographics['age_groups']['Under 18'] += 1
                elif age < 25:
                    demographics['age_groups']['18-24'] += 1
                elif age < 35:
                    demographics['age_groups']['25-34'] += 1
                elif age < 50:
                    demographics['age_groups']['35-49'] += 1
                elif age < 65:
                    demographics['age_groups']['50-64'] += 1
                else:
                    demographics['age_groups']['65+'] += 1
            
            # Employment
            employment = client.get('employment_status', client.get('moneyAndResources', {}).get('workSituation', 'Unknown'))
            demographics['employment_status'][employment] += 1
            
            # Veteran status
            is_veteran = client.get('is_veteran', client.get('personalCharacteristics', {}).get('veteran', 'No'))
            demographics['veteran_status'][str(is_veteran)] += 1
            
            # Language (from intake submissions)
            if client.get('source') == 'patient_intake_app':
                language = client.get('personalCharacteristics', {}).get('language', 'Unknown')
                demographics['language'][language] += 1
                
                # Race/ethnicity
                hispanic = client.get('personalCharacteristics', {}).get('hispanicLatino', 'Unknown')
                race = client.get('personalCharacteristics', {}).get('race', [])
                if hispanic == 'Yes':
                    demographics['race_ethnicity']['Hispanic/Latino'] += 1
                elif isinstance(race, list) and race:
                    for r in race:
                        demographics['race_ethnicity'][r] += 1
        
        return {k: dict(v) for k, v in demographics.items()}
    
    def _analyze_risk_distribution(self, risk_assessments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze risk level distribution."""
        risk_levels = defaultdict(int)
        risk_percentages = []
        factor_scores = defaultdict(list)
        
        for assessment in risk_assessments:
            risk_levels[assessment['risk_level']] += 1
            risk_percentages.append(assessment['risk_percentage'])
            
            # Collect factor scores
            for factor_name, factor_data in assessment['risk_factors'].items():
                factor_scores[factor_name].append(factor_data['score'])
        
        # Calculate statistics
        avg_risk = statistics.mean(risk_percentages) if risk_percentages else 0
        median_risk = statistics.median(risk_percentages) if risk_percentages else 0
        
        # Factor analysis
        factor_analysis = {}
        for factor_name, scores in factor_scores.items():
            if scores:
                factor_analysis[factor_name] = {
                    'average_score': statistics.mean(scores),
                    'max_score': max(scores),
                    'high_risk_count': sum(1 for s in scores if s > statistics.mean(scores))
                }
        
        return {
            'risk_level_distribution': dict(risk_levels),
            'average_risk_percentage': round(avg_risk, 1),
            'median_risk_percentage': round(median_risk, 1),
            'highest_risk_percentage': max(risk_percentages) if risk_percentages else 0,
            'lowest_risk_percentage': min(risk_percentages) if risk_percentages else 0,
            'factor_analysis': factor_analysis
        }
    
    def _analyze_resource_usage(self, clients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze resource usage patterns."""
        category_usage = defaultdict(int)
        status_distribution = defaultdict(int)
        monthly_trends = defaultdict(int)
        
        total_resources = 0
        
        for client in clients:
            resources = client.get('resources', [])
            total_resources += len(resources)
            
            for resource in resources:
                category = resource.get('category', 'other')
                category_usage[category] += 1
                
                status = resource.get('status', 'pending')
                status_distribution[status] += 1
                
                # Monthly trends
                added_date_str = resource.get('added_date', '')
                if added_date_str:
                    try:
                        added_date = datetime.fromisoformat(added_date_str.replace('Z', '+00:00'))
                        month_key = added_date.strftime('%Y-%m')
                        monthly_trends[month_key] += 1
                    except:
                        continue
        
        return {
            'total_resources_assigned': total_resources,
            'category_distribution': dict(category_usage),
            'status_distribution': dict(status_distribution),
            'monthly_trends': dict(monthly_trends),
            'average_resources_per_client': round(total_resources / len(clients), 2) if clients else 0
        }
    
    def _analyze_client_needs(self, clients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze client needs patterns."""
        needs_frequency = defaultdict(int)
        urgent_needs = defaultdict(int)
        
        for client in clients:
            # Regular client needs
            needs = client.get('needs', [])
            if isinstance(needs, list):
                for need in needs:
                    needs_frequency[need] += 1
            
            # Intake submission needs
            if client.get('source') == 'patient_intake_app':
                basic_needs = client.get('basicNeeds', {})
                unable_to_get = basic_needs.get('unableToGet', {})
                
                for need, has_need in unable_to_get.items():
                    if has_need:
                        needs_frequency[f"unable_to_get_{need}"] += 1
                        
                        # Mark as urgent if high stress
                        stress_level = basic_needs.get('stressLevel', '')
                        if stress_level in ['High', 'Very High']:
                            urgent_needs[f"unable_to_get_{need}"] += 1
        
        return {
            'needs_frequency': dict(needs_frequency),
            'urgent_needs': dict(urgent_needs),
            'most_common_needs': sorted(needs_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        }
    
    def _analyze_geographic_distribution(self, clients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze geographic distribution of clients."""
        cities = defaultdict(int)
        zip_codes = defaultdict(int)
        
        for client in clients:
            # Regular address
            address = client.get('address', '')
            if address:
                # Extract city and zip from address
                parts = address.split(',')
                if len(parts) >= 2:
                    city_state_zip = parts[-1].strip()
                    if 'TX' in city_state_zip:
                        cities['Houston area'] += 1
            
            # Intake submission address
            if client.get('source') == 'patient_intake_app':
                family_housing = client.get('familyAndHousing', {})
                address_info = family_housing.get('address', {})
                
                city = address_info.get('city', '')
                zip_code = address_info.get('zipCode', '')
                
                if city:
                    cities[city] += 1
                if zip_code:
                    zip_codes[zip_code] += 1
        
        return {
            'city_distribution': dict(cities),
            'zip_code_distribution': dict(zip_codes)
        }
    
    def _analyze_outcomes(self, clients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze client outcomes and resource effectiveness."""
        successful_outcomes = 0
        in_progress = 0
        needs_attention = 0
        
        resource_effectiveness = defaultdict(lambda: {'total': 0, 'successful': 0})
        
        for client in clients:
            resources = client.get('resources', [])
            client_outcome = 'unknown'
            
            if resources:
                statuses = [r.get('status', 'pending') for r in resources]
                if 'completed' in statuses or 'successful' in statuses:
                    successful_outcomes += 1
                    client_outcome = 'successful'
                elif 'in_progress' in statuses or 'active' in statuses:
                    in_progress += 1
                    client_outcome = 'in_progress'
                else:
                    needs_attention += 1
                    client_outcome = 'needs_attention'
                
                # Track resource effectiveness
                for resource in resources:
                    category = resource.get('category', 'other')
                    status = resource.get('status', 'pending')
                    
                    resource_effectiveness[category]['total'] += 1
                    if status in ['completed', 'successful']:
                        resource_effectiveness[category]['successful'] += 1
        
        # Calculate effectiveness rates
        effectiveness_rates = {}
        for category, data in resource_effectiveness.items():
            if data['total'] > 0:
                effectiveness_rates[category] = round((data['successful'] / data['total']) * 100, 1)
        
        return {
            'outcome_distribution': {
                'successful': successful_outcomes,
                'in_progress': in_progress,
                'needs_attention': needs_attention
            },
            'resource_effectiveness_rates': effectiveness_rates
        }
    
    def _calculate_age(self, date_of_birth: str) -> Optional[int]:
        """Calculate age from date of birth string."""
        if not date_of_birth:
            return None
        
        try:
            birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except:
            return None 