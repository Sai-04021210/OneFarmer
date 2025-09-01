from odoo import api, fields, models, _
from datetime import datetime, date


class PlantMonitor(models.Model):
    _name = 'plant.monitor'
    _description = 'Plant Monitor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Plant Name', required=True, tracking=True)
    scientific_name = fields.Char(string='Scientific Name', tracking=True)
    plant_type = fields.Selection([
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('herb', 'Herb'),
        ('grain', 'Grain'),
        ('flower', 'Flower'),
        ('tree', 'Tree'),
        ('other', 'Other')
    ], string='Plant Type', default='vegetable', required=True, tracking=True)
    
    plant_variety = fields.Selection([
        ('tomato', 'Tomato'), ('lettuce', 'Lettuce'), ('cucumber', 'Cucumber'),
        ('pepper', 'Pepper'), ('onion', 'Onion'), ('carrot', 'Carrot'),
        ('broccoli', 'Broccoli'), ('cabbage', 'Cabbage'), ('spinach', 'Spinach'),
        ('potato', 'Potato'), ('eggplant', 'Eggplant'), ('zucchini', 'Zucchini'),
        ('apple', 'Apple'), ('orange', 'Orange'), ('banana', 'Banana'),
        ('strawberry', 'Strawberry'), ('grape', 'Grape'), ('mango', 'Mango'),
        ('cherry', 'Cherry'), ('peach', 'Peach'), ('watermelon', 'Watermelon'),
        ('basil', 'Basil'), ('mint', 'Mint'), ('parsley', 'Parsley'),
        ('cilantro', 'Cilantro'), ('rosemary', 'Rosemary'), ('thyme', 'Thyme'),
        ('oregano', 'Oregano'), ('sage', 'Sage'), ('dill', 'Dill'),
        ('wheat', 'Wheat'), ('rice', 'Rice'), ('corn', 'Corn'),
        ('barley', 'Barley'), ('oats', 'Oats'), ('quinoa', 'Quinoa'),
        ('rose', 'Rose'), ('sunflower', 'Sunflower'), ('tulip', 'Tulip'),
        ('marigold', 'Marigold'), ('daisy', 'Daisy'), ('lily', 'Lily'),
        ('oak', 'Oak'), ('pine', 'Pine'), ('maple', 'Maple'),
        ('birch', 'Birch'), ('cedar', 'Cedar'), ('willow', 'Willow')
    ], string='Plant Variety', tracking=True)
    
    # Location Information
    location = fields.Char(string='Location/Field', tracking=True)
    plot_number = fields.Char(string='Plot Number', tracking=True)
    coordinates = fields.Char(string='GPS Coordinates', tracking=True)
    
    # Planting Information
    planting_date = fields.Date(string='Planting Date', default=fields.Date.today, tracking=True)
    expected_harvest_date = fields.Date(string='Expected Harvest Date', tracking=True)
    actual_harvest_date = fields.Date(string='Actual Harvest Date', tracking=True)
    
    # Plant Status with detailed stages
    status = fields.Selection([
        ('seed_prep', 'Seed Preparation'),
        ('germination', 'Germination'),
        ('seedling', 'Seedling'),
        ('transplant', 'Transplant Ready'),
        ('vegetative', 'Vegetative Growth'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('ripening', 'Ripening'),
        ('mature', 'Mature'),
        ('harvested', 'Harvested'),
        ('dead', 'Dead')
    ], string='Growth Stage', default='seed_prep', required=True, tracking=True)
    
    # Detailed substage based on plant type
    substage = fields.Selection([
        ('seed_selection', 'Seed Selection'),
        ('medium_prep', 'Medium Preparation'),
        ('day_1_5', 'Days 1-5'),
        ('day_6_10', 'Days 6-10'),
        ('cotyledon', 'Cotyledon Stage'),
        ('first_true_leaves', 'First True Leaves'),
        ('2_3_leaves', '2-3 True Leaves'),
        ('hardening_off', 'Hardening Off'),
        ('ready_transplant', 'Ready for Transplant'),
        ('early_growth', 'Early Growth'),
        ('rapid_growth', 'Rapid Growth'),
        ('pre_flowering', 'Pre-Flowering'),
        ('bud_formation', 'Bud Formation'),
        ('early_flowering', 'Early Flowering'),
        ('full_bloom', 'Full Bloom'),
        ('fruit_set', 'Fruit Set'),
        ('young_fruit', 'Young Fruit Development'),
        ('fruit_expansion', 'Fruit Expansion'),
        ('color_change', 'Color Change'),
        ('softening', 'Softening'),
        ('full_ripe', 'Fully Ripe')
    ], string='Substage', tracking=True)
    
    health_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical')
    ], string='Health Status', default='good', tracking=True)
    
    # Measurements
    height = fields.Float(string='Height (cm)', tracking=True)
    width = fields.Float(string='Width (cm)', tracking=True)
    
    # Detailed Cultivation Information
    sowing_medium = fields.Selection([
        ('seed_tray', 'Seed Tray'),
        ('peat_pots', 'Peat Pots'), 
        ('direct_soil', 'Direct Soil'),
        ('hydroponic', 'Hydroponic'),
        ('rockwool', 'Rockwool'),
        ('coco_coir', 'Coco Coir')
    ], string='Sowing Medium', tracking=True)
    
    seed_depth = fields.Float(string='Seed Depth (cm)', help='Depth at which seeds were planted', tracking=True)
    spacing_between_plants = fields.Float(string='Plant Spacing (cm)', help='Distance between plants', tracking=True)
    
    # Environmental conditions
    soil_temperature = fields.Float(string='Soil Temperature (°C)', tracking=True)
    ambient_temperature = fields.Float(string='Ambient Temperature (°C)', tracking=True)
    soil_ph = fields.Float(string='Soil pH', tracking=True)
    
    # Season and timing
    growing_season = fields.Selection([
        ('spring', 'Spring'),
        ('summer', 'Summer'), 
        ('fall', 'Fall'),
        ('winter', 'Winter'),
        ('year_round', 'Year Round')
    ], string='Growing Season', tracking=True)
    
    days_to_germination = fields.Integer(string='Days to Germination', compute='_compute_growth_days')
    days_to_transplant = fields.Integer(string='Days to Transplant', compute='_compute_growth_days')
    days_to_flowering = fields.Integer(string='Days to Flowering', compute='_compute_growth_days')
    days_to_harvest = fields.Integer(string='Days to Harvest', compute='_compute_growth_days')
    
    # Care Information
    watering_frequency = fields.Selection([
        ('twice_daily', 'Twice Daily'),
        ('daily', 'Daily'),
        ('every_2_days', 'Every 2 Days'),
        ('every_3_days', 'Every 3 Days'),
        ('weekly', 'Weekly'),
        ('bi_weekly', 'Bi-Weekly'),
        ('monthly', 'Monthly')
    ], string='Watering Frequency', default='daily', tracking=True)
    
    watering_amount = fields.Float(string='Watering Amount (ml)', help='Amount of water per watering session', tracking=True)
    fertilizer_type = fields.Char(string='Fertilizer Type', tracking=True)
    fertilizer_schedule = fields.Selection([
        ('weekly', 'Weekly'),
        ('bi_weekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
        ('as_needed', 'As Needed')
    ], string='Fertilizer Schedule', tracking=True)
    
    last_watered = fields.Date(string='Last Watered')
    last_fertilized = fields.Date(string='Last Fertilized')
    
    # Notes and Observations
    notes = fields.Text(string='Notes')
    observations = fields.Text(string='Recent Observations', tracking=True)
    
    # Related Records
    monitoring_logs = fields.One2many('plant.monitoring.log', 'plant_id', string='Monitoring Logs')
    log_count = fields.Integer(string='Log Count', compute='_compute_log_count')
    
    @api.depends('monitoring_logs')
    def _compute_log_count(self):
        for record in self:
            record.log_count = len(record.monitoring_logs)
    
    
    @api.depends('plant_type', 'planting_date')
    def _compute_growth_days(self):
        """Compute expected days for different growth stages based on plant type"""
        for record in self:
            if record.plant_type:
                days_data = self._get_growth_timeline(record.plant_type)
                record.days_to_germination = days_data.get('germination', 7)
                record.days_to_transplant = days_data.get('transplant', 21)
                record.days_to_flowering = days_data.get('flowering', 45)
                record.days_to_harvest = days_data.get('harvest', 90)
            else:
                record.days_to_germination = 0
                record.days_to_transplant = 0
                record.days_to_flowering = 0
                record.days_to_harvest = 0
    
    def _get_substage_options(self, plant_type, status):
        """Get substage options based on plant type and current status"""
        substages = {
            'vegetable': {
                'seed_prep': [('seed_selection', 'Seed Selection'), ('medium_prep', 'Medium Preparation')],
                'germination': [('day_1_5', 'Days 1-5'), ('day_6_10', 'Days 6-10')],
                'seedling': [('cotyledon', 'Cotyledon Stage'), ('first_true_leaves', 'First True Leaves'), ('2_3_leaves', '2-3 True Leaves')],
                'transplant': [('hardening_off', 'Hardening Off'), ('ready_transplant', 'Ready for Transplant')],
                'vegetative': [('early_growth', 'Early Growth'), ('rapid_growth', 'Rapid Growth'), ('pre_flowering', 'Pre-Flowering')],
                'flowering': [('bud_formation', 'Bud Formation'), ('early_flowering', 'Early Flowering'), ('full_bloom', 'Full Bloom')],
                'fruiting': [('fruit_set', 'Fruit Set'), ('young_fruit', 'Young Fruit Development'), ('fruit_expansion', 'Fruit Expansion')],
                'ripening': [('color_change', 'Color Change'), ('softening', 'Softening'), ('full_ripe', 'Fully Ripe')]
            },
            'fruit': {
                'seed_prep': [('seed_selection', 'Seed Selection'), ('stratification', 'Cold Stratification')],
                'germination': [('day_1_10', 'Days 1-10'), ('day_11_21', 'Days 11-21')],
                'seedling': [('cotyledon', 'Cotyledon Stage'), ('first_leaves', 'First True Leaves'), ('young_plant', 'Young Plant')],
                'transplant': [('root_development', 'Root Development'), ('hardening_off', 'Hardening Off')],
                'vegetative': [('trunk_formation', 'Trunk Formation'), ('branch_development', 'Branch Development'), ('canopy_formation', 'Canopy Formation')],
                'flowering': [('bud_break', 'Bud Break'), ('bloom', 'Bloom'), ('petal_fall', 'Petal Fall')],
                'fruiting': [('fruit_set', 'Fruit Set'), ('cell_division', 'Cell Division'), ('cell_enlargement', 'Cell Enlargement')],
                'ripening': [('color_break', 'Color Break'), ('sugar_development', 'Sugar Development'), ('harvest_ready', 'Harvest Ready')]
            },
            'herb': {
                'seed_prep': [('seed_selection', 'Seed Selection'), ('medium_prep', 'Medium Preparation')],
                'germination': [('day_1_7', 'Days 1-7'), ('day_8_14', 'Days 8-14')],
                'seedling': [('cotyledon', 'Cotyledon Stage'), ('first_leaves', 'First True Leaves')],
                'transplant': [('root_bound', 'Root Bound'), ('transplant_ready', 'Transplant Ready')],
                'vegetative': [('bushing_out', 'Bushing Out'), ('leaf_production', 'Leaf Production'), ('stem_strengthening', 'Stem Strengthening')],
                'flowering': [('flower_buds', 'Flower Buds'), ('early_bloom', 'Early Bloom'), ('full_flower', 'Full Flower')],
                'fruiting': [('seed_formation', 'Seed Formation'), ('seed_development', 'Seed Development')],
                'ripening': [('seed_maturity', 'Seed Maturity'), ('harvest_time', 'Harvest Time')]
            }
        }
        return substages.get(plant_type, {}).get(status, [])
    
    def _get_variety_options(self, plant_type):
        """Get variety options based on plant type"""
        varieties = {
            'vegetable': [
                ('tomato', 'Tomato'), ('lettuce', 'Lettuce'), ('cucumber', 'Cucumber'),
                ('pepper', 'Pepper'), ('onion', 'Onion'), ('carrot', 'Carrot'),
                ('broccoli', 'Broccoli'), ('cabbage', 'Cabbage'), ('spinach', 'Spinach'),
                ('potato', 'Potato'), ('eggplant', 'Eggplant'), ('zucchini', 'Zucchini')
            ],
            'fruit': [
                ('apple', 'Apple'), ('orange', 'Orange'), ('banana', 'Banana'),
                ('strawberry', 'Strawberry'), ('grape', 'Grape'), ('mango', 'Mango'),
                ('cherry', 'Cherry'), ('peach', 'Peach'), ('watermelon', 'Watermelon')
            ],
            'herb': [
                ('basil', 'Basil'), ('mint', 'Mint'), ('parsley', 'Parsley'),
                ('cilantro', 'Cilantro'), ('rosemary', 'Rosemary'), ('thyme', 'Thyme'),
                ('oregano', 'Oregano'), ('sage', 'Sage'), ('dill', 'Dill')
            ],
            'grain': [
                ('wheat', 'Wheat'), ('rice', 'Rice'), ('corn', 'Corn'),
                ('barley', 'Barley'), ('oats', 'Oats'), ('quinoa', 'Quinoa')
            ],
            'flower': [
                ('rose', 'Rose'), ('sunflower', 'Sunflower'), ('tulip', 'Tulip'),
                ('marigold', 'Marigold'), ('daisy', 'Daisy'), ('lily', 'Lily')
            ],
            'tree': [
                ('oak', 'Oak'), ('pine', 'Pine'), ('maple', 'Maple'),
                ('birch', 'Birch'), ('cedar', 'Cedar'), ('willow', 'Willow')
            ]
        }
        return varieties.get(plant_type, [])
    
    def _get_growth_timeline(self, plant_type):
        """Get growth timeline in days for different plant types"""
        timelines = {
            'vegetable': {'germination': 7, 'transplant': 21, 'flowering': 45, 'harvest': 75},
            'fruit': {'germination': 14, 'transplant': 60, 'flowering': 120, 'harvest': 180},
            'herb': {'germination': 5, 'transplant': 14, 'flowering': 30, 'harvest': 45},
            'grain': {'germination': 10, 'transplant': 30, 'flowering': 60, 'harvest': 120},
            'flower': {'germination': 7, 'transplant': 21, 'flowering': 35, 'harvest': 60},
            'tree': {'germination': 21, 'transplant': 90, 'flowering': 365, 'harvest': 730}
        }
        return timelines.get(plant_type, {'germination': 7, 'transplant': 21, 'flowering': 45, 'harvest': 90})
    
    def _get_cultivation_defaults(self, plant_type):
        """Get cultivation defaults for specific plant types like tomato"""
        defaults = {
            'vegetable': {
                'tomato': {
                    'sowing_medium': 'seed_tray',
                    'seed_depth': 0.6,  # 0.6cm (1/4 inch)
                    'spacing_between_plants': 60,  # 60cm (2 feet)
                    'soil_temperature': 24,  # 24°C (75°F)
                    'watering_frequency': 'daily',
                    'watering_amount': 250,  # 250ml
                    'fertilizer_type': 'Balanced NPK 10-10-10',
                    'fertilizer_schedule': 'bi_weekly',
                    'growing_season': 'summer',
                    'soil_ph': 6.2
                },
                'lettuce': {
                    'sowing_medium': 'seed_tray',
                    'seed_depth': 0.3,
                    'spacing_between_plants': 20,
                    'soil_temperature': 18,
                    'watering_frequency': 'daily',
                    'watering_amount': 100,
                    'fertilizer_type': 'High Nitrogen',
                    'fertilizer_schedule': 'weekly',
                    'growing_season': 'spring',
                    'soil_ph': 6.5
                }
            }
        }
        return defaults.get(plant_type, {})
    
    def _get_stage_specific_content(self, plant_variety, status):
        """Get stage-specific content for plant variety"""
        
        tomato_content = {
            'seed_prep': {
                'notes': """🍅 TOMATO - SEED PREPARATION STAGE
                
CURRENT TASKS:
✓ Select high-quality tomato seeds (heirloom or hybrid)
✓ Prepare seed starting trays with quality potting mix
✓ Set up growing area with heat mat (24°C soil temperature)
✓ Prepare labels for variety tracking

SEED PREPARATION STEPS:
1. Choose disease-resistant varieties for your climate
2. Optional: Soak seeds 24hrs in lukewarm water
3. Fill seed trays with sterile potting mix
4. Plant seeds 0.6cm (1/4") deep, 2-3 seeds per cell
5. Cover lightly with vermiculite or fine soil
6. Mist gently to moisten soil

ENVIRONMENTAL REQUIREMENTS:
- Soil temperature: 21-26°C (70-80°F) 
- Air temperature: 18-24°C (65-75°F)
- Humidity: 70-80%
- Light: Not required until germination

NEXT STAGE: Germination (5-10 days)""",
                'observations': "Seeds prepared and planted. Monitoring for germination signs."
            },
            
            'germination': {
                'notes': """🍅 TOMATO - GERMINATION STAGE (Days 1-10)
                
CURRENT FOCUS:
✓ Monitor for seed emergence daily
✓ Maintain consistent soil moisture and temperature
✓ Watch for cotyledon (seed leaf) emergence
✓ Remove any failed seeds after 10 days

DAILY CARE:
- Check soil moisture (should be damp, not soggy)
- Maintain heat mat at 24°C
- Ensure good air circulation
- Mist if surface appears dry

SIGNS OF SUCCESS:
- Day 3-5: Radicle (root) emergence
- Day 5-8: Stem emergence from soil
- Day 7-10: Cotyledon leaves unfold
- Healthy seedlings are thick-stemmed and upright

TROUBLESHOOTING:
- No emergence after 10 days = seed failure
- Leggy seedlings = need more light
- Damping off = too much moisture/poor air circulation

NEXT STAGE: Seedling (when cotyledons fully open)""",
                'observations': "Monitoring germination progress. Seeds should emerge within 5-10 days."
            },
            
            'seedling': {
                'notes': """🍅 TOMATO - SEEDLING STAGE (Weeks 2-4)
                
CURRENT PRIORITIES:
✓ Provide adequate light (14-16 hours daily)
✓ Begin fertilization after first true leaves
✓ Monitor for pest issues (aphids, whitefly)
✓ Prepare for transplanting

CARE REQUIREMENTS:
- Light: LED grow lights 2-3 inches above seedlings
- Water: When top soil feels dry, water thoroughly
- Fertilizer: Start weak liquid fertilizer (1/4 strength)
- Temperature: 18-21°C day, 15-18°C night

GROWTH MILESTONES:
- Week 2: First true leaves appear
- Week 3: 2-3 sets of true leaves
- Week 4: Ready for transplant or potting up

CRITICAL ACTIONS:
1. Thin to strongest seedling per cell
2. Begin hardening off process in week 4
3. Watch for early blight or fungal issues
4. Prepare larger pots or garden bed

NEXT STAGE: Transplant Ready (when 2-3 true leaf sets)""",
                'observations': "Seedlings developing true leaves. Beginning fertilization schedule."
            },
            
            'transplant': {
                'notes': """🍅 TOMATO - TRANSPLANT STAGE (Weeks 4-6)
                
TRANSPLANT READINESS:
✓ 2-3 sets of true leaves developed
✓ Stems are thick and sturdy (pencil thickness)
✓ Night temperatures consistently above 10°C
✓ Last frost date has passed

HARDENING OFF PROCESS (Week 1):
Day 1-2: Outside 2-3 hours in shade
Day 3-4: Outside 4-5 hours, morning sun
Day 5-6: Outside 6-8 hours, more sun exposure
Day 7: Full day outside if weather permits

TRANSPLANTING STEPS:
1. Prepare soil: well-draining, pH 6.0-6.8
2. Dig holes 60cm apart, deeper than root ball
3. Bury 2/3 of stem (roots will grow from buried stem)
4. Water thoroughly after transplanting
5. Install tomato cages or stakes immediately

POST-TRANSPLANT CARE:
- Water deeply 2-3 times per week
- Mulch around plants to retain moisture
- Watch for transplant shock (wilting)
- Begin weekly feeding after 1 week

NEXT STAGE: Vegetative Growth (after establishment)""",
                'observations': "Preparing for transplant. Hardening off seedlings to outdoor conditions."
            },
            
            'vegetative': {
                'notes': """🍅 TOMATO - VEGETATIVE GROWTH STAGE (Weeks 6-10)
                
GROWTH FOCUS:
✓ Rapid leaf and stem development
✓ Strong root system establishment
✓ Branch formation and structure building
✓ Preparation for flower production

WEEKLY TASKS:
- Deep watering 2-3 times (avoid overhead watering)
- Side-shoot pruning on indeterminate varieties
- Tie stems to supports as they grow
- Apply balanced fertilizer (NPK 10-10-10) bi-weekly

PLANT TRAINING:
- Remove suckers (shoots between main stem and branches)
- Tie main stem to stake every 15-20cm of growth
- Remove lower leaves touching soil
- Maintain single or double stem system

MONITORING POINTS:
- Height growth: 30-60cm per month
- Leaf color: Deep green (pale = needs nitrogen)
- Stem thickness: Should be robust, not spindly
- Pest watch: Hornworms, aphids, whiteflies

ENVIRONMENTAL NEEDS:
- Temperature: 21-26°C day, 15-18°C night
- Water: 2.5-5cm per week (including rainfall)
- Support: Stakes, cages, or trellising system

NEXT STAGE: Flowering (when first flower clusters appear)""",
                'observations': "Plant establishing vigorous growth. Monitoring stem development and pruning suckers."
            },
            
            'flowering': {
                'notes': """🍅 TOMATO - FLOWERING STAGE (Weeks 8-12)
                
FLOWERING PRIORITIES:
✓ Support flower cluster development
✓ Ensure proper pollination conditions
✓ Adjust nutrition for fruit production
✓ Monitor for blossom end rot prevention

NUTRITION SHIFT:
- Reduce nitrogen, increase phosphorus and potassium
- Switch to bloom fertilizer (5-10-10 or similar)
- Add calcium supplement to prevent blossom end rot
- Maintain consistent watering (no drought stress)

POLLINATION SUPPORT:
- Shake plants gently daily to aid pollination
- Maintain proper air circulation
- Ideal temperature: 18-24°C for pollen viability
- Humidity: 65-75% for optimal pollen release

FLOWER CARE:
- Don't remove flower clusters unless plant is stressed
- Watch for early flowers to drop (normal in heat)
- Support heavy flower trusses with clips
- Continue removing suckers and lower leaves

COMMON ISSUES:
- Flower drop: Usually temperature or water stress
- No fruit set: Poor pollination or nutrient imbalance
- Catfacing: Cool weather during flower development
- Blossom end rot: Calcium deficiency/inconsistent watering

NEXT STAGE: Fruiting (when small fruits are visible)""",
                'observations': "First flower clusters forming. Adjusting nutrition for fruit development phase."
            },
            
            'fruiting': {
                'notes': """🍅 TOMATO - FRUITING STAGE (Weeks 10-16)
                
FRUIT DEVELOPMENT FOCUS:
✓ Support developing fruit weight
✓ Optimize nutrition for fruit size and quality
✓ Monitor for fruit diseases and disorders
✓ Begin harvest planning

CRITICAL CARE:
- Consistent deep watering (never let soil fully dry)
- Support heavy fruit trusses with clips or slings
- Continue calcium applications
- Increase potassium for fruit quality

FRUIT MONITORING:
- Size development: Ping-pong to tennis ball size
- Color: Should remain green and firm
- Shape: Watch for cracking, catfacing, or deformities
- Health: Check for early blight, late blight spots

PLANT MANAGEMENT:
- Continue sucker removal on indeterminates
- Remove leaves below lowest fruit cluster
- Maintain 4-6 main fruit trusses per plant
- Top plants when desired height is reached

HARVEST PREPARATION:
- First fruits typically ready 20-30 days after fruit set
- Plan for daily harvesting once ripening begins
- Prepare storage and processing plans
- Consider succession planting for continuous harvest

NEXT STAGE: Ripening (when fruits begin color change)""",
                'observations': "Small green fruits developing well. Monitoring for proper sizing and disease prevention."
            },
            
            'ripening': {
                'notes': """🍅 TOMATO - RIPENING STAGE (Weeks 12-20)
                
RIPENING MANAGEMENT:
✓ Monitor daily for harvest-ready fruits
✓ Adjust watering to concentrate flavors
✓ Remove aging lower leaves
✓ Plan for preservation and storage

HARVEST INDICATORS:
- Color change: Green to pink to full color
- Firmness: Slight give when gently squeezed  
- Glossy appearance with full color development
- Easy separation from vine with gentle twist

QUALITY OPTIMIZATION:
- Reduce watering slightly to concentrate flavors
- Remove some leaves to expose fruits to sunlight
- Harvest at "breaker" stage for shipping/storage
- Pick fully ripe for immediate consumption

DAILY TASKS:
- Check all fruit trusses for ripe tomatoes
- Remove any overripe, cracked, or diseased fruits
- Support heavy branches with additional ties
- Continue removing suckers and excess foliage

POST-HARVEST CARE:
- Clean hands/tools between plants to prevent disease
- Store ripe tomatoes at room temperature
- Green tomatoes can ripen indoors
- Save seeds from best fruits for next season

SEASON END PLANNING:
- Plan final harvest before first frost
- Consider green tomato preservation methods
- Prepare beds for fall/winter crops
- Compost healthy plant material after harvest

NEXT STAGE: Mature/Harvested (full production mode)""",
                'observations': "Fruits changing color and approaching harvest. Daily monitoring for optimal ripeness."
            },
            
            'mature': {
                'notes': """🍅 TOMATO - MATURE/HARVEST STAGE (Peak Production)
                
PEAK HARVEST MANAGEMENT:
✓ Daily harvesting of ripe fruits
✓ Continuous plant maintenance
✓ Disease prevention during harvest
✓ Yield tracking and quality assessment

HARVEST BEST PRACTICES:
- Pick early morning when cool for best flavor
- Twist and pull gently, or use clean shears
- Harvest at proper ripeness for intended use
- Handle carefully to prevent bruising

ONGOING PLANT CARE:
- Continue deep, infrequent watering
- Monthly fertilization with potassium-rich blend
- Remove diseased or dying foliage promptly
- Maintain plant support systems

QUALITY CONTROL:
- Sort fruits by ripeness and intended use
- Remove any fruits showing signs of disease
- Track yields for garden planning
- Save seeds from best-performing plants

STORAGE & PRESERVATION:
- Fresh: Room temperature for 3-5 days
- Extended storage: Cool, dry location
- Processing: Sauce, paste, canning, freezing
- Seed saving: Ferment seeds from ripe fruits

END OF SEASON:
- Continue harvesting until first frost
- Pick green tomatoes before frost for ripening indoors
- Remove and compost healthy plant materials
- Plan crop rotation for next season

FINAL STAGE: Season complete, plan for next year!""",
                'observations': "Peak harvest season. Daily collection of ripe tomatoes and ongoing plant maintenance."
            }
        }
        
        # Add content for other varieties (lettuce, pepper, etc.)
        lettuce_content = {
            'seed_prep': {
                'notes': """🥬 LETTUCE - SEED PREPARATION STAGE
                
SEED PREP TASKS:
✓ Select appropriate variety for season (heat-tolerant for summer)
✓ Prepare seed trays or direct sow area
✓ Cool soil if planting in warm weather
✓ Plan for succession planting every 2 weeks

PLANTING DETAILS:
- Seed depth: 0.3cm (1/8 inch) - lettuce needs light to germinate
- Soil temperature: 15-20°C (optimal for germination)
- Spacing: 15-20cm apart for head lettuce, 10cm for leaf
- Location: Partial shade in hot climates

NEXT STAGE: Germination (2-7 days)""",
                'observations': "Lettuce seeds prepared. Quick germination expected in cool conditions."
            },
            'germination': {
                'notes': """🥬 LETTUCE - GERMINATION STAGE (Days 1-7)
                
GERMINATION CARE:
✓ Keep soil consistently moist but not waterlogged
✓ Provide light immediately upon emergence
✓ Maintain cool temperatures (below 25°C)
✓ Thin overcrowded seedlings early

OPTIMAL CONDITIONS:
- Temperature: 15-18°C for best germination
- Moisture: Light, frequent watering
- Light: Bright but not intense (lettuce prefers cool light)

NEXT STAGE: Seedling development""",
                'observations': "Seeds germinating rapidly. Monitoring for proper emergence and thinning."
            }
        }
        
        # Combine all variety content
        content_database = {
            'tomato': tomato_content,
            'lettuce': lettuce_content,
            # Add more varieties as needed
        }
        
        variety_content = content_database.get(plant_variety, {})
        return variety_content.get(status, {
            'notes': f"""📋 {plant_variety.upper()} - {status.upper().replace('_', ' ')} STAGE
            
GENERAL CARE:
- Monitor plant health daily
- Maintain consistent watering schedule  
- Watch for pest and disease issues
- Follow proper fertilization program
            
STAGE-SPECIFIC TASKS:
- Complete tasks appropriate for current growth stage
- Prepare for next stage transition
- Record observations for future reference""",
            'observations': f"Plant in {status.replace('_', ' ')} stage. Monitor progress and adjust care as needed."
        })
    
    @api.onchange('planting_date', 'plant_type')
    def _onchange_expected_harvest(self):
        """Auto-calculate expected harvest date based on plant type"""
        if self.planting_date and self.plant_type:
            harvest_days = {
                'vegetable': 60,  # 2 months average
                'fruit': 120,     # 4 months average
                'herb': 45,       # 1.5 months average
                'grain': 90,      # 3 months average
                'flower': 75,     # 2.5 months average
                'tree': 365,      # 1 year average
                'other': 90       # 3 months default
            }
            days_to_add = harvest_days.get(self.plant_type, 90)
            self.expected_harvest_date = fields.Date.add(self.planting_date, days=days_to_add)
    
    def action_view_monitoring_logs(self):
        """Action to view monitoring logs for this plant"""
        return {
            'name': _('Monitoring Logs - %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'plant.monitoring.log',
            'view_mode': 'tree,form',
            'domain': [('plant_id', '=', self.id)],
            'context': {'default_plant_id': self.id},
        }
    
    def advance_to_next_stage(self):
        """Advance plant to next growth stage"""
        stage_progression = {
            'seed_prep': 'germination',
            'germination': 'seedling',
            'seedling': 'transplant',
            'transplant': 'vegetative',
            'vegetative': 'flowering',
            'flowering': 'fruiting',
            'fruiting': 'ripening',
            'ripening': 'mature',
            'mature': 'harvested'
        }
        
        if self.status in stage_progression:
            old_stage = self.status
            self.status = stage_progression[self.status]
            self.message_post(
                body=_('Plant stage advanced from %s to %s') % (
                    dict(self._fields['status'].selection).get(old_stage, old_stage),
                    dict(self._fields['status'].selection).get(self.status, self.status)
                )
            )
    
    def set_stage(self, stage):
        """Set plant to a specific stage with validation and logging"""
        if stage in dict(self._fields['status'].selection):
            old_stage = self.status
            self.status = stage
            self.message_post(
                body=_('Plant stage changed from %s to %s') % (
                    dict(self._fields['status'].selection).get(old_stage, old_stage),
                    dict(self._fields['status'].selection).get(stage, stage)
                )
            )
            return True
        return False
    
    def action_set_seedling(self):
        """Set plant stage to seedling"""
        return self.set_stage('seedling')
    
    def action_set_growing(self):
        """Set plant stage to growing"""
        return self.set_stage('growing')
    
    def action_set_flowering(self):
        """Set plant stage to flowering"""
        return self.set_stage('flowering')
    
    def action_set_fruiting(self):
        """Set plant stage to fruiting"""
        return self.set_stage('fruiting')
    
    def action_set_mature(self):
        """Set plant stage to mature"""
        return self.set_stage('mature')
    
    def action_set_harvested(self):
        """Set plant stage to harvested"""
        return self.set_stage('harvested')
    
    def apply_cultivation_defaults(self):
        """Apply cultivation defaults based on plant variety"""
        if self.plant_type and self.plant_variety:
            defaults = self._get_cultivation_defaults(self.plant_type).get(self.plant_variety, {})
            
            for field, value in defaults.items():
                if hasattr(self, field) and not getattr(self, field):
                    setattr(self, field, value)
    
    @api.onchange('plant_variety')
    def _onchange_plant_variety(self):
        """Auto-apply cultivation defaults when variety changes"""
        if self.plant_variety:
            self.apply_cultivation_defaults()
            self._update_stage_specific_content()
    
    @api.onchange('status')
    def _onchange_status(self):
        """Update content when stage changes"""
        if self.status:
            self._update_stage_specific_content()
            self._update_substage_options()
    
    def _update_substage_options(self):
        """Update available substages based on current status and plant type"""
        if self.plant_type and self.status:
            available_substages = self._get_substage_options(self.plant_type, self.status)
            if available_substages:
                # Set the first relevant substage as default
                self.substage = available_substages[0][0]
    
    def _update_stage_specific_content(self):
        """Update notes and observations based on current stage and plant variety"""
        if self.plant_variety and self.status:
            content = self._get_stage_specific_content(self.plant_variety, self.status)
            if content:
                self.notes = content['notes']
                self.observations = content['observations']
        
    @api.model
    def auto_advance_plant_stages(self):
        """Automatically advance plant stages based on age and other criteria"""
        today = fields.Date.today()
        
        # Auto-advance seedlings after 14 days
        seedlings = self.search([
            ('status', '=', 'seedling'),
            ('planting_date', '<=', fields.Date.subtract(today, days=14))
        ])
        for plant in seedlings:
            plant.status = 'growing'
            plant.message_post(body=_('Plant automatically advanced to Growing stage after 14 days'))
        
        # Auto-advance growing plants based on plant type
        growing_plants = self.search([('status', '=', 'growing')])
        for plant in growing_plants:
            if plant.planting_date:
                days_old = (today - plant.planting_date).days
                
                # Different flowering times for different plant types
                flowering_days = {
                    'vegetable': 30,
                    'fruit': 45,
                    'herb': 25,
                    'grain': 40,
                    'flower': 20,
                    'tree': 180,
                    'other': 35
                }
                
                required_days = flowering_days.get(plant.plant_type, 35)
                if days_old >= required_days:
                    plant.status = 'flowering'
                    plant.message_post(body=_('Plant automatically advanced to Flowering stage'))
        
        # Auto-advance flowering to fruiting after additional time
        flowering_plants = self.search([('status', '=', 'flowering')])
        for plant in flowering_plants:
            if plant.planting_date:
                days_old = (today - plant.planting_date).days
                
                fruiting_days = {
                    'vegetable': 45,
                    'fruit': 75,
                    'herb': 35,
                    'grain': 60,
                    'flower': 30,
                    'tree': 220,
                    'other': 50
                }
                
                required_days = fruiting_days.get(plant.plant_type, 50)
                if days_old >= required_days:
                    plant.status = 'fruiting'
                    plant.message_post(body=_('Plant automatically advanced to Fruiting stage'))


class PlantMonitoringLog(models.Model):
    _name = 'plant.monitoring.log'
    _description = 'Plant Monitoring Log'
    _order = 'log_date desc'

    plant_id = fields.Many2one('plant.monitor', string='Plant', required=True, ondelete='cascade')
    log_date = fields.Date(string='Log Date', default=fields.Date.today, required=True)
    log_time = fields.Datetime(string='Log Time', default=fields.Datetime.now, required=True)
    
    # Environmental Data
    temperature = fields.Float(string='Temperature (°C)')
    humidity = fields.Float(string='Humidity (%)')
    soil_moisture = fields.Float(string='Soil Moisture (%)')
    light_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Light Level')
    
    # Plant Measurements
    height = fields.Float(string='Height (cm)')
    width = fields.Float(string='Width (cm)')
    
    # Activities
    watered = fields.Boolean(string='Watered')
    fertilized = fields.Boolean(string='Fertilized')
    pruned = fields.Boolean(string='Pruned')
    
    # Health Observations
    health_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical')
    ], string='Health Status')
    
    pest_issues = fields.Boolean(string='Pest Issues')
    disease_issues = fields.Boolean(string='Disease Issues')
    
    notes = fields.Text(string='Notes')
    image = fields.Binary(string='Photo')
    
    # Update parent plant with latest data
    @api.model
    def create(self, vals):
        log = super(PlantMonitoringLog, self).create(vals)
        if log.plant_id:
            update_vals = {}
            if log.height:
                update_vals['height'] = log.height
            if log.width:
                update_vals['width'] = log.width
            if log.health_status:
                update_vals['health_status'] = log.health_status
            if log.watered:
                update_vals['last_watered'] = log.log_date
            if log.fertilized:
                update_vals['last_fertilized'] = log.log_date
            
            if update_vals:
                log.plant_id.write(update_vals)
        
        return log