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
    
    # Location Information
    location = fields.Char(string='Location/Field', tracking=True)
    plot_number = fields.Char(string='Plot Number', tracking=True)
    coordinates = fields.Char(string='GPS Coordinates', tracking=True)
    
    # Planting Information
    planting_date = fields.Date(string='Planting Date', default=fields.Date.today, tracking=True)
    expected_harvest_date = fields.Date(string='Expected Harvest Date', tracking=True)
    actual_harvest_date = fields.Date(string='Actual Harvest Date', tracking=True)
    
    # Plant Status
    status = fields.Selection([
        ('seedling', 'Seedling'),
        ('growing', 'Growing'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('mature', 'Mature'),
        ('harvested', 'Harvested'),
        ('dead', 'Dead')
    ], string='Status', default='seedling', required=True, tracking=True)
    
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
    
    # Care Information
    watering_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('every_2_days', 'Every 2 Days'),
        ('weekly', 'Weekly'),
        ('bi_weekly', 'Bi-Weekly'),
        ('monthly', 'Monthly')
    ], string='Watering Frequency', default='daily')
    
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