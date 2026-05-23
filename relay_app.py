#!/usr/bin/env python3
"""
RELAY Mobile App Mockup
Premium mobile operations app for smart asset movement and live zone tracking
"""

import customtkinter as ctk
from tkinter import font
import tkinter as tk

# Configure CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RELAYApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_window()
        self.setup_colors()
        self.setup_fonts()
        self.setup_navigation_state()
        self.create_main_layout()
        self.build_current_screen()
        
    def setup_navigation_state(self):
        """Initialize navigation state"""
        self.sidebar_open = False
        self.current_screen = "Command Center"
        self.current_role = "Logistics"
        self.sidebar_frame = None
        self.overlay_frame = None
        
        self.navigation_items = [
            ("Command Center", "🏠"),
            ("Live Map", "🌍"),
            ("Scanner", "📱"),
            ("Event Planner", "📅"),
            ("Asset 360", "📦"),
            ("Alerts", "🔔"),
            ("Analytics", "📊"),
            ("Audit Mode", "🔍"),
        ]
        
        self.role_options = ["Logistics", "Finance", "Events"]
        
        # Event planner state
        self.setup_event_planner_state()
        
        # Shared app state for assets
        self.setup_shared_state()
        self.setup_role_configurations()
        
    def setup_event_planner_state(self):
        """Initialize event planner state"""
        self.active_deployments = {}
        self.event_form_data = {
            "event_name": "",
            "event_date": "",
            "from_zone": "Storage Room B",
            "to_zone": "Main Hall",
            "chairs_needed": "100",
            "tables_needed": "10",
            "projectors_needed": "2",
            "speakers_needed": "2",
            "return_time": "6 hours"
        }
        
    def setup_role_configurations(self):
        """Configure role-specific content and colors"""
        self.role_configs = {
            "Logistics": {
                "theme_color": "#00A3FF",  # Blue/cyan
                "secondary_color": "#0088CC", 
                "accent_color": "#00FF88",
                "warning_color": "#FFB800",
                "kpis": [
                    ("Active Deployments", "2", "#00A3FF"),
                    ("Assets In Transit", "128", "#00FF88"), 
                    ("Rooms With Issues", "3", "#FFB800")
                ],
                "quick_actions": [
                    "🚛 Deploy Event Setup",
                    "📦 Move Room Setup", 
                    "↩️ Return Assets"
                ],
                "insights": [
                    "Chair Batch-4 delayed 12 minutes in transit",
                    "Storage Room B operating at 95% capacity",
                    "3 active movement routes require coordination",
                    "Main Hall receiving deployment EV-A231"
                ],
                "focus": "Movement coordination and asset logistics",
                "map_emphasis": "movement",
                "screen_title": "Logistics Operations Center"
            },
            "Finance": {
                "theme_color": "#00D084",  # Green/gold
                "secondary_color": "#FFD700",
                "accent_color": "#32CD32", 
                "warning_color": "#FF6B35",
                "kpis": [
                    ("Infrastructure Value", "$2.4M", "#00D084"),
                    ("Underutilized Assets", "42 items", "#FF6B35"),
                    ("Depreciation Risk", "$180K", "#FFD700")
                ],
                "quick_actions": [
                    "💰 Generate Cost Report",
                    "📊 Review Asset Usage",
                    "⚠️ Replacement Planning"
                ],
                "insights": [
                    "$450K in assets unused for 30+ days",
                    "Projector fleet ROI exceeds 340% annually", 
                    "Storage Room A contains $890K in equipment",
                    "Chair utilization rate: 87% (above target)"
                ],
                "focus": "Asset value optimization and financial intelligence",
                "map_emphasis": "value",
                "screen_title": "Financial Asset Intelligence"
            },
            "Events": {
                "theme_color": "#8B5CF6",  # Purple/magenta
                "secondary_color": "#EC4899",
                "accent_color": "#A855F7",
                "warning_color": "#F59E0B",
                "kpis": [
                    ("Active Events", "3", "#8B5CF6"),
                    ("Setup Completion", "82%", "#00FF88"),
                    ("Assets Pending Arrival", "2", "#F59E0B")
                ],
                "quick_actions": [
                    "🎯 Create Event",
                    "📅 Deploy Event Setup", 
                    "✅ Verify Returns"
                ],
                "insights": [
                    "Annual Conference setup: 82% complete",
                    "2 projectors delayed for Conference Room",
                    "Event Hall ready for next deployment",
                    "Board Meeting requires 15 additional chairs"
                ],
                "focus": "Event readiness and deployment coordination",
                "map_emphasis": "events", 
                "screen_title": "Event Coordination Center"
            }
        }
        
    def setup_shared_state(self):
        """Initialize shared application state"""
        self.assets = {
            # Pre-populated demo assets with utilization data
            "RFID-CH-2001": {
                "id": "RFID-CH-2001",
                "type": "Chair",
                "product_name": "Standard Event Chair",
                "zone": "Storage Room A",
                "condition": "Good",
                "status": "Available",
                "department": "Logistics",
                "icon": "🪑",
                "last_updated": "1 hour ago",
                "utilization": {
                    "usage_score": 87,  # 0-100 score
                    "deployments_30_days": 12,
                    "idle_days": 3,
                    "total_usage_hours": 145,
                    "efficiency_rating": "High"
                }
            },
            "RFID-TB-3002": {
                "id": "RFID-TB-3002", 
                "type": "Table",
                "product_name": "Folding Event Table",
                "zone": "Storage Room B",
                "condition": "Good", 
                "status": "Available",
                "department": "Logistics",
                "icon": "🪑",
                "last_updated": "3 hours ago",
                "utilization": {
                    "usage_score": 34,
                    "deployments_30_days": 2,
                    "idle_days": 18,
                    "total_usage_hours": 24,
                    "efficiency_rating": "Low"
                }
            },
            "RFID-PR-4003": {
                "id": "RFID-PR-4003",
                "type": "Projector", 
                "product_name": "Epson Projector Kit",
                "zone": "Main Hall",
                "condition": "Good",
                "status": "In Use",
                "department": "Events", 
                "icon": "📽️",
                "last_updated": "30 min ago",
                "utilization": {
                    "usage_score": 94,
                    "deployments_30_days": 28,
                    "idle_days": 0,
                    "total_usage_hours": 340,
                    "efficiency_rating": "Excellent"
                }
            }
        }
        
        # Generate utilization insights
        self.generate_utilization_insights()
        self.assets = {
            # Pre-populated demo assets with utilization data
            "RFID-CH-2001": {
                "id": "RFID-CH-2001",
                "type": "Chair",
                "product_name": "Standard Event Chair",
                "zone": "Storage Room A",
                "condition": "Good",
                "status": "Available",
                "department": "Logistics",
                "icon": "🪑",
                "last_updated": "1 hour ago",
                "utilization": {
                    "usage_score": 87,  # 0-100 score
                    "deployments_30_days": 12,
                    "idle_days": 3,
                    "total_usage_hours": 145,
                    "efficiency_rating": "High"
                }
            },
            "RFID-TB-3002": {
                "id": "RFID-TB-3002", 
                "type": "Table",
                "product_name": "Folding Event Table",
                "zone": "Storage Room B",
                "condition": "Good", 
                "status": "Available",
                "department": "Logistics",
                "icon": "🪑",
                "last_updated": "3 hours ago",
                "utilization": {
                    "usage_score": 34,
                    "deployments_30_days": 2,
                    "idle_days": 18,
                    "total_usage_hours": 24,
                    "efficiency_rating": "Low"
                }
            },
            "RFID-PR-4003": {
                "id": "RFID-PR-4003",
                "type": "Projector", 
                "product_name": "Epson Projector Kit",
                "zone": "Main Hall",
                "condition": "Good",
                "status": "In Use",
                "department": "Events", 
                "icon": "📽️",
                "last_updated": "30 min ago",
                "utilization": {
                    "usage_score": 94,
                    "deployments_30_days": 28,
                    "idle_days": 0,
                    "total_usage_hours": 340,
                    "efficiency_rating": "Excellent"
                }
            }
        }
        
        # Generate utilization insights
        self.generate_utilization_insights()
        
    def generate_utilization_insights(self):
        """Generate utilization insights from asset data"""
        self.utilization_insights = {
            "underutilized_assets": 42,  # Assets with low usage scores
            "high_demand_rooms": ["Storage Room B", "Main Hall"],
            "idle_assets_30_days": 15,
            "fleet_utilizations": {
                "chairs": 87,
                "tables": 34, 
                "projectors": 94,
                "speakers": 78
            },
            "efficiency_alerts": [
                "42 chairs unused for 30+ days",
                "Projector fleet utilization exceeds 90%", 
                "Storage Room B under heavy demand",
                "Conference Room assets underutilized by 45%"
            ],
            "optimization_opportunities": [
                "Redistribute 25 idle chairs to high-demand zones",
                "Replace underperforming tables in Storage Room A",
                "Add 2 more projectors to meet growing demand"
            ]
        }
        
        # Zone asset counts for quick lookup
        self.update_zone_counts()
        
    def update_zone_counts(self):
        """Update asset counts by zone"""
        self.zone_counts = {
            "Storage Room A": {"chairs": 0, "tables": 0, "projectors": 0, "speakers": 0, "tvs": 0, "laptops": 0, "total": 0},
            "Storage Room B": {"chairs": 0, "tables": 0, "projectors": 0, "speakers": 0, "tvs": 0, "laptops": 0, "total": 0},
            "Main Hall": {"chairs": 0, "tables": 0, "projectors": 0, "speakers": 0, "tvs": 0, "laptops": 0, "total": 0},
            "Conference Room": {"chairs": 0, "tables": 0, "projectors": 0, "speakers": 0, "tvs": 0, "laptops": 0, "total": 0},
            "Lab 4": {"chairs": 0, "tables": 0, "projectors": 0, "speakers": 0, "tvs": 0, "laptops": 0, "total": 0},
            "Loading Area": {"chairs": 0, "tables": 0, "projectors": 0, "speakers": 0, "tvs": 0, "laptops": 0, "total": 0},
            "Event Hall": {"chairs": 0, "tables": 0, "projectors": 0, "speakers": 0, "tvs": 0, "laptops": 0, "total": 0}
        }
        
        # Add demo bulk assets for visual demonstration
        self.zone_counts["Storage Room A"]["chairs"] = 124
        self.zone_counts["Storage Room A"]["tables"] = 18
        self.zone_counts["Storage Room A"]["total"] = 142
        
        self.zone_counts["Storage Room B"]["chairs"] = 96
        self.zone_counts["Storage Room B"]["tables"] = 22  
        self.zone_counts["Storage Room B"]["projectors"] = 4
        self.zone_counts["Storage Room B"]["total"] = 122
        
        self.zone_counts["Main Hall"]["chairs"] = 80
        self.zone_counts["Main Hall"]["tables"] = 6
        self.zone_counts["Main Hall"]["projectors"] = 2
        self.zone_counts["Main Hall"]["total"] = 88
        
        self.zone_counts["Conference Room"]["chairs"] = 12
        self.zone_counts["Conference Room"]["tables"] = 3
        self.zone_counts["Conference Room"]["tvs"] = 1
        self.zone_counts["Conference Room"]["total"] = 16
        
        # Count actual registered assets
        for asset in self.assets.values():
            zone = asset["zone"]
            if zone in self.zone_counts:
                asset_type = asset["type"].lower()
                if "chair" in asset_type:
                    self.zone_counts[zone]["chairs"] += 1
                elif "table" in asset_type:
                    self.zone_counts[zone]["tables"] += 1
                elif "projector" in asset_type:
                    self.zone_counts[zone]["projectors"] += 1
                elif "speaker" in asset_type:
                    self.zone_counts[zone]["speakers"] += 1
                elif "tv" in asset_type or "screen" in asset_type:
                    self.zone_counts[zone]["tvs"] += 1
                elif "laptop" in asset_type:
                    self.zone_counts[zone]["laptops"] += 1
                    
                self.zone_counts[zone]["total"] += 1
        
    def setup_window(self):
        """Configure the mobile-sized window"""
        self.root.title("RELAY")
        self.root.geometry("390x844")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (390 // 2)
        y = (self.root.winfo_screenheight() // 2) - (844 // 2)
        self.root.geometry(f"390x844+{x}+{y}")
        
    def setup_colors(self):
        """Define the premium dark theme colors"""
        self.colors = {
            'bg_primary': '#0F0F0F',
            'bg_secondary': '#1A1A1A',
            'bg_card': '#222222',
            'bg_sidebar': '#141824',  # Premium glassmorphism sidebar
            'bg_overlay': '#0A0E18',  # Very light, cinematic overlay (like iOS)
            'accent_blue': '#00A3FF',
            'accent_green': '#00FF88',
            'text_primary': '#FFFFFF',
            'text_secondary': '#CCCCCC',
            'text_muted': '#888888',
            'success': '#00FF88',
            'warning': '#FFB800',
            'error': '#FF4444',
            'glow': '#00A3FF'  # Bright blue for accents
        }
        
    def setup_fonts(self):
        """Define typography hierarchy"""
        self.fonts = {
            'heading_large': ('SF Pro Display', 28, 'bold'),
            'heading_medium': ('SF Pro Display', 22, 'bold'),
            'heading_small': ('SF Pro Display', 18, 'bold'),
            'body_large': ('SF Pro Text', 16, 'normal'),
            'body_medium': ('SF Pro Text', 14, 'normal'),
            'body_small': ('SF Pro Text', 12, 'normal'),
            'caption': ('SF Pro Text', 11, 'normal'),
            'icon': ('SF Pro Text', 18, 'normal')
        }
        
    def create_main_layout(self):
        """Create the main app layout structure"""
        # Main container
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color=self.colors['bg_primary'],
            corner_radius=0
        )
        self.main_container.pack(fill="both", expand=True)
        
        # Header
        self.create_header()
        
        # Content area (scrollable)
        self.content_frame = ctk.CTkScrollableFrame(
            self.main_container,
            fg_color=self.colors['bg_primary'],
            corner_radius=0
        )
        self.content_frame.pack(fill="both", expand=True)
        
    def create_header(self):
        """Create the modern mobile header"""
        self.header_frame = ctk.CTkFrame(
            self.main_container,
            height=70,
            fg_color=self.colors['bg_secondary'],
            corner_radius=0
        )
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Hamburger menu button (left)
        self.hamburger_btn = ctk.CTkButton(
            self.header_frame,
            text="≡",
            width=40,
            height=40,
            font=('SF Pro Display', 20, 'normal'),
            fg_color="transparent",
            text_color=self.colors['text_primary'],
            hover_color=self.colors['bg_card'],
            corner_radius=8,
            command=self.toggle_sidebar
        )
        self.hamburger_btn.pack(side="left", padx=20, pady=15)
        
        # Page title (center)
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=self.current_screen,
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary']
        )
        self.title_label.pack(pady=25)
        
        # Right side container
        right_container = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent"
        )
        right_container.pack(side="right", padx=20, pady=15)
        
        # Notification icon
        notif_btn = ctk.CTkButton(
            right_container,
            text="🔔",
            width=40,
            height=40,
            font=self.fonts['body_medium'],
            fg_color=self.colors['bg_card'],
            text_color=self.colors['text_primary'],
            hover_color=self.colors['bg_primary'],
            corner_radius=20
        )
        notif_btn.pack(side="right")
        
        # Live indicator
        if self.current_screen in ["Command Center", "Live Map"]:
            live_frame = ctk.CTkFrame(
                right_container,
                height=28,
                fg_color=self.colors['success'],
                corner_radius=14
            )
            live_frame.pack(side="right", padx=(0, 10))
            
            live_label = ctk.CTkLabel(
                live_frame,
                text="● LIVE",
                font=self.fonts['caption'],
                text_color=self.colors['bg_primary']
            )
            live_label.pack(padx=10, pady=4)
            
    def toggle_sidebar(self):
        """Toggle the sidebar visibility with smooth animation"""
        if self.sidebar_open:
            self.close_sidebar()
        else:
            self.open_sidebar()
            
    def open_sidebar(self):
        """Open the sidebar with glassmorphism effect"""
        self.sidebar_open = True
        
        # Create full-screen overlay that covers entire app
        self.overlay_frame = ctk.CTkFrame(
            self.root,
            width=390,
            height=844,
            fg_color=self.colors['bg_overlay'],
            corner_radius=0
        )
        self.overlay_frame.place(x=0, y=0)
        self.overlay_frame.bind("<Button-1>", lambda e: self.close_sidebar())
        
        # Create premium glassmorphism sidebar (75% of screen width = ~290px)
        sidebar_width = int(390 * 0.75)  # 75% of screen width
        self.sidebar_frame = ctk.CTkFrame(
            self.root,
            width=sidebar_width,
            height=844,
            fg_color=self.colors['bg_sidebar'],  # Premium glassmorphism color
            corner_radius=20,  # Rounded right corners for premium feel
            border_width=2,  # Slightly thicker border for depth
            border_color=self.colors['glow']
        )
        self.sidebar_frame.place(x=0, y=0)
        
        self.build_sidebar()
        
    def close_sidebar(self):
        """Close the sidebar"""
        if self.sidebar_frame:
            self.sidebar_frame.destroy()
            self.sidebar_frame = None
            
        if self.overlay_frame:
            self.overlay_frame.destroy()
            self.overlay_frame = None
            
        self.sidebar_open = False
        
    def build_sidebar(self):
        """Build the sidebar content"""
        if not self.sidebar_frame:
            return
            
        # Sidebar header with logo
        sidebar_header = ctk.CTkFrame(
            self.sidebar_frame,
            height=80,
            fg_color="transparent"
        )
        sidebar_header.pack(fill="x", padx=20, pady=(20, 0))
        sidebar_header.pack_propagate(False)
        
        # RELAY logo
        logo_label = ctk.CTkLabel(
            sidebar_header,
            text="RELAY",
            font=('SF Pro Display', 24, 'bold'),
            text_color=self.colors['accent_blue']
        )
        logo_label.pack(pady=25)
        
        # Interactive Role Switcher
        role_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=12
        )
        role_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Role switcher header
        role_header = ctk.CTkLabel(
            role_frame,
            text="Department Role",
            font=self.fonts['body_small'],
            text_color=self.colors['text_muted']
        )
        role_header.pack(pady=(12, 8))
        
        # Role pills/buttons
        roles_container = ctk.CTkFrame(role_frame, fg_color="transparent")
        roles_container.pack(fill="x", padx=12, pady=(0, 12))
        
        for role in self.role_options:
            is_current = role == self.current_role
            role_config = self.role_configs.get(role, {})
            theme_color = role_config.get("theme_color", self.colors['accent_blue'])
            
            role_btn = ctk.CTkButton(
                roles_container,
                text=role,
                height=32,
                font=self.fonts['body_small'],
                fg_color=theme_color if is_current else "transparent",
                text_color=self.colors['text_primary'],
                hover_color=theme_color,
                corner_radius=16,
                border_width=1,
                border_color=theme_color,
                command=lambda r=role: self.switch_role(r)
            )
            role_btn.pack(pady=2, fill="x")
        
        # Navigation items — use reusable create_nav_item() for pixel-perfect alignment
        sidebar_width = int(390 * 0.75)  # matches open_sidebar calculation
        nav_container = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color="transparent"
        )
        nav_container.pack(fill="x", padx=12, pady=(0, 20))

        role_config = self.role_configs.get(self.current_role, {})
        active_color = role_config.get("theme_color", self.colors['accent_blue'])

        for item_name, icon in self.navigation_items:
            is_active = item_name == self.current_screen
            self.create_nav_item(
                parent=nav_container,
                icon=icon,
                label=item_name,
                page_name=item_name,
                is_active=is_active,
                active_color=active_color,
                sidebar_width=sidebar_width
            )

        # Bottom section
        bottom_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color="transparent"
        )
        bottom_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        # Settings
        settings_btn = ctk.CTkButton(
            bottom_frame,
            text="⚙️  Settings",
            height=40,
            font=self.fonts['body_medium'],
            fg_color="transparent",
            text_color=self.colors['text_muted'],
            hover_color=self.colors['bg_card'],
            corner_radius=8,
            anchor="w"
        )
        settings_btn.pack(fill="x", pady=(0, 8))

        # Logout
        logout_btn = ctk.CTkButton(
            bottom_frame,
            text="↗️  Logout",
            height=40,
            font=self.fonts['body_medium'],
            fg_color="transparent",
            text_color=self.colors['text_muted'],
            hover_color=self.colors['bg_card'],
            corner_radius=8,
            anchor="w"
        )
        logout_btn.pack(fill="x")

    def create_nav_item(self, parent, icon, label, page_name, is_active, active_color, sidebar_width):
        """
        Reusable nav item builder — pixel-perfect alignment for every sidebar row.

        Layout constants (all rows are identical):
          - row height       : 44px
          - left margin      : 12px
          - icon frame width : 26px  (hard-clips emoji, centering it inside)
          - icon-text gap    : 8px
          - text x-start     : 12 + 26 + 8 = 46px from row left edge (always)
          - right margin     : 12px
          - active state     : blue background only — padding/sizes never change
        """
        ROW_HEIGHT    = 44
        LEFT_MARGIN   = 12
        ICON_WIDTH    = 26
        ICON_TEXT_GAP = 8
        RIGHT_MARGIN  = 12

        # Background: blue when active, transparent otherwise
        bg_color = active_color if is_active else "transparent"

        # ── Row frame (full width, fixed height) ─────────────────────────────
        row = ctk.CTkFrame(
            parent,
            height=ROW_HEIGHT,
            fg_color=bg_color,
            corner_radius=10
        )
        row.pack(fill="x", pady=(0, 4))
        row.pack_propagate(False)

        # ── Icon container — true 26×26 square, centered vertically in 44px row ──
        #    pack_propagate(False) hard-clips to exactly 26×26 so NO emoji glyph
        #    can bleed outside and affect layout.
        #    pady = (ROW_HEIGHT - ICON_WIDTH) // 2 = (44-26)//2 = 9 → vertical center.
        ICON_VPAD = (ROW_HEIGHT - ICON_WIDTH) // 2  # = 9px top & bottom

        icon_frame = ctk.CTkFrame(
            row,
            width=ICON_WIDTH,
            height=ICON_WIDTH,          # ← square: 26×26
            fg_color="transparent"
        )
        icon_frame.pack(side="left", padx=(LEFT_MARGIN, 0), pady=ICON_VPAD)
        icon_frame.pack_propagate(False)

        icon_lbl = ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=('SF Pro Text', 16, 'normal'),
            text_color=self.colors['text_primary'],
            anchor="center",
            width=ICON_WIDTH,
            height=ICON_WIDTH
        )
        # fill="both" + expand=True fills the fixed 26×26 square completely,
        # then anchor="center" draws every glyph centered within that square.
        icon_lbl.pack(fill="both", expand=True)

        # ── Text label — always starts at x = LEFT_MARGIN + ICON_WIDTH + GAP ─
        text_lbl = ctk.CTkLabel(
            row,
            text=label,
            font=self.fonts['body_medium'],
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        text_lbl.pack(side="left", padx=(ICON_TEXT_GAP, RIGHT_MARGIN))

        # ── Click binding ─────────────────────────────────────────────────────
        click_cmd = lambda e, s=page_name: self.navigate_to(s)
        for w in [row, icon_frame, icon_lbl, text_lbl]:
            w.bind("<Button-1>", click_cmd)

        # ── Hover effect for inactive items ───────────────────────────────────
        if not is_active:
            hover_in  = lambda e, f=row: f.configure(fg_color=self.colors['bg_card'])
            hover_out = lambda e, f=row: f.configure(fg_color="transparent")
            for w in [row, icon_frame, icon_lbl, text_lbl]:
                w.bind("<Enter>", hover_in)
                w.bind("<Leave>", hover_out)

        return row

    def switch_role(self, new_role):
        """Switch to a different department role"""
        if new_role != self.current_role:
            self.current_role = new_role
            self.close_sidebar()
            self.build_current_screen()  # Rebuild screen with new role context

    def navigate_to(self, screen_name):
        """Navigate to a different screen"""
        self.current_screen = screen_name
        self.title_label.configure(text=screen_name)
        self.close_sidebar()
        self.build_current_screen()
        
    def build_current_screen(self):
        """Build the current screen content"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if self.current_screen == "Command Center":
            self.build_command_center()
        elif self.current_screen == "Live Map":
            self.build_live_map()
        elif self.current_screen == "Scanner":
            self.build_scanner()
        elif self.current_screen == "Event Planner":
            self.build_event_planner()
        elif self.current_screen == "Audit Mode":
            self.build_audit_mode()
        else:
            self.build_placeholder_screen()
            
    def build_command_center(self):
        """Build the role-aware Command Center screen"""
        # Get current role configuration
        role_config = self.role_configs.get(self.current_role, self.role_configs["Logistics"])
        
        # Main title section with role-specific focus
        title_container = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        title_container.pack(fill="x", padx=20, pady=(20, 15))
        
        # Role-specific screen title
        screen_title = role_config.get("screen_title", f"{self.current_role} Command Center")
        role_indicator = ctk.CTkLabel(
            title_container,
            text=screen_title,
            font=self.fonts['heading_small'],
            text_color=role_config.get("theme_color", self.colors['accent_blue']),
            anchor="w"
        )
        role_indicator.pack(fill="x")
        
        # Focus description
        focus_label = ctk.CTkLabel(
            title_container,
            text=role_config.get("focus", "Live zone awareness for QSTP assets"),
            font=self.fonts['body_large'],
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        focus_label.pack(fill="x", pady=(5, 0))
        
        # Role-specific KPI Cards (2+1 layout)
        kpi_container = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        kpi_container.pack(fill="x", padx=20, pady=(15, 30))
        
        # Get KPIs from role configuration
        kpis = role_config.get("kpis", [])
        
        # First row - 2 cards
        for i in range(min(2, len(kpis))):
            title, value, color = kpis[i]
            kpi_card = self.create_kpi_card(kpi_container, title, value, color)
            kpi_card.grid(row=0, column=i, padx=(0, 10 if i == 0 else 0), 
                         pady=(0, 15), sticky="ew")
        
        # Second row - 1 card (if exists)
        if len(kpis) > 2:
            title, value, color = kpis[2]
            kpi_card = self.create_kpi_card(kpi_container, title, value, color)
            kpi_card.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        kpi_container.grid_columnconfigure(0, weight=1)
        kpi_container.grid_columnconfigure(1, weight=1)
        
        # Role-specific Quick Actions
        self.create_quick_actions()
        
        # Role-specific Insights
        self.create_role_insights()
        
        # Live Activity
        self.create_live_activity()
        
    def create_role_insights(self):
        """Create role-specific insights section"""
        role_config = self.role_configs.get(self.current_role, self.role_configs["Logistics"])
        insights = role_config.get("insights", [])
        
        if not insights:
            return
            
        insights_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        insights_frame.pack(fill="x", padx=20, pady=(0, 30))
        
        # Section title
        title_label = ctk.CTkLabel(
            insights_frame,
            text=f"{self.current_role} Insights",
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 15))
        
        # Insights items
        for insight in insights:
            insight_item = ctk.CTkFrame(
                insights_frame,
                height=50,
                fg_color=self.colors['bg_card'],
                corner_radius=12,
                border_width=1,
                border_color=role_config.get("theme_color", self.colors['accent_blue'])
            )
            insight_item.pack(fill="x", pady=(0, 8))
            insight_item.pack_propagate(False)
            
            # Insight icon based on role
            role_icons = {
                "Logistics": "🚚",
                "Finance": "💰",
                "Events": "🎯"
            }
            
            icon_label = ctk.CTkLabel(
                insight_item,
                text=role_icons.get(self.current_role, "📊"),
                font=self.fonts['body_large'],
                text_color=role_config.get("theme_color", self.colors['accent_blue'])
            )
            icon_label.pack(side="left", padx=(20, 15), pady=15)
            
            insight_label = ctk.CTkLabel(
                insight_item,
                text=insight,
                font=self.fonts['body_medium'],
                text_color=self.colors['text_primary'],
                anchor="w"
            )
            insight_label.pack(side="left", fill="x", expand=True, pady=15)
        
    def build_live_map(self):
        """Build the premium Live Map with smart building visualization"""
        # Map filters
        filters_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        filters_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        filter_chips = ["All", "Chairs", "Tables", "Electronics", "Damaged", "In Transit"]
        for chip in filter_chips:
            chip_btn = ctk.CTkButton(
                filters_frame,
                text=chip,
                height=30,
                width=60,
                font=self.fonts['caption'],
                fg_color=self.colors['bg_card'] if chip != "All" else self.colors['accent_blue'],
                text_color=self.colors['text_primary'],
                hover_color=self.colors['accent_blue'],
                corner_radius=15
            )
            chip_btn.pack(side="left", padx=(0, 8))
        
        # Main map container - premium smart building view
        map_container = ctk.CTkFrame(
            self.content_frame,
            height=500,
            fg_color=self.colors['bg_card'],
            corner_radius=16,
            border_width=1,
            border_color=self.colors['glow']
        )
        map_container.pack(fill="x", padx=15, pady=(0, 15))
        map_container.pack_propagate(False)
        
        # Build the visual floor plan
        self.create_floor_plan(map_container)
        
        # Live deployment status
        deployment_frame = ctk.CTkFrame(
            self.content_frame,
            height=80,
            fg_color=self.colors['bg_secondary'],
            corner_radius=16
        )
        deployment_frame.pack(fill="x", padx=15, pady=(0, 20))
        deployment_frame.pack_propagate(False)
        
        # Active deployment indicator
        deployment_header = ctk.CTkLabel(
            deployment_frame,
            text="🔄 Active Deployment",
            font=self.fonts['heading_small'],
            text_color=self.colors['accent_green']
        )
        deployment_header.pack(pady=(15, 5))
        
        deployment_status = ctk.CTkLabel(
            deployment_frame,
            text="Storage Room B → Main Hall • Chair Batch x25",
            font=self.fonts['body_medium'],
            text_color=self.colors['text_secondary']
        )
        deployment_status.pack()
        
    def create_floor_plan(self, parent):
        """Create the visual QSTP floor plan"""
        # Floor plan grid container
        floor_frame = ctk.CTkFrame(parent, fg_color="transparent")
        floor_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create rooms in a realistic layout
        rooms_config = [
            # (name, row, col, width, height, room_type)
            ("Storage Room A", 0, 0, 1, 1, "storage"),
            ("Storage Room B", 0, 1, 1, 1, "storage"), 
            ("Loading Area", 0, 2, 1, 1, "loading"),
            ("Main Hall", 1, 0, 2, 1, "hall"),
            ("Conference Room", 1, 2, 1, 1, "conference"),
            ("Lab 4", 2, 0, 1, 1, "lab"),
            ("Event Hall", 2, 1, 2, 1, "event")
        ]
        
        for room_name, row, col, width, height, room_type in rooms_config:
            room_card = self.create_room_card(floor_frame, room_name, room_type)
            room_card.grid(row=row, column=col, columnspan=width, rowspan=height,
                          padx=2, pady=2, sticky="ew")
            
        # Configure grid weights for responsive layout
        for i in range(3):
            floor_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            floor_frame.grid_rowconfigure(i, weight=1)
            
    def create_room_card(self, parent, room_name, room_type):
        """Create an interactive room card with asset visualization"""
        # Get room data from shared state
        room_data = self.zone_counts.get(room_name, {"total": 0, "chairs": 0, "tables": 0, "projectors": 0})
        
        # Determine room status color based on assets
        status_color = self.colors['accent_green']  # Default: Active
        status_text = "READY"
        
        if room_data["total"] > 100:
            status_color = self.colors['accent_blue']
            status_text = "ACTIVE"
        elif room_data["total"] < 10:
            status_color = self.colors['text_muted']
            status_text = "MINIMAL"
            
        # Create room card
        room_frame = ctk.CTkFrame(
            parent,
            height=120,
            fg_color=self.get_room_color(room_type),
            corner_radius=12,
            border_width=1,
            border_color=status_color
        )
        room_frame.pack_propagate(False)
        
        # Room header
        header_frame = ctk.CTkFrame(room_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=8, pady=(8, 4))
        
        # Room name and status
        name_label = ctk.CTkLabel(
            header_frame,
            text=room_name.replace(" Room ", " "),
            font=self.fonts['body_medium'],
            text_color=self.colors['text_primary']
        )
        name_label.pack(side="left")
        
        status_label = ctk.CTkLabel(
            header_frame,
            text=status_text,
            font=self.fonts['caption'],
            text_color=status_color
        )
        status_label.pack(side="right")
        
        # Asset count and breakdown
        count_label = ctk.CTkLabel(
            room_frame,
            text=f"{room_data['total']} assets",
            font=self.fonts['body_large'],
            text_color=self.colors['accent_blue']
        )
        count_label.pack(pady=(0, 4))
        
        # Asset breakdown
        breakdown_parts = []
        if room_data["chairs"] > 0:
            breakdown_parts.append(f"🪑{room_data['chairs']}")
        if room_data["tables"] > 0:
            breakdown_parts.append(f"🪑{room_data['tables']}")
        if room_data["projectors"] > 0:
            breakdown_parts.append(f"📽️{room_data['projectors']}")
        if room_data["tvs"] > 0:
            breakdown_parts.append(f"📺{room_data['tvs']}")
            
        breakdown_text = " • ".join(breakdown_parts[:3])  # Limit to 3 items
        if breakdown_text:
            breakdown_label = ctk.CTkLabel(
                room_frame,
                text=breakdown_text,
                font=self.fonts['body_small'],
                text_color=self.colors['text_secondary']
            )
            breakdown_label.pack(pady=(0, 8))
            
        # Make room clickable
        room_frame.bind("<Button-1>", lambda e: self.show_room_details(room_name))
        
        # Add visual room type indicators
        self.add_room_visual_elements(room_frame, room_type)
        
        return room_frame
        
    def get_room_color(self, room_type):
        """Get background color based on room type"""
        room_colors = {
            "storage": "#2A2A2A",    # Darker for storage
            "hall": "#1F2937",       # Slightly blue for halls
            "conference": "#2D1B69", # Purple tint for meeting spaces
            "lab": "#1E3A28",        # Green tint for labs
            "loading": "#3A2617",    # Brown tint for loading
            "event": "#2A1E3A"       # Deep purple for events
        }
        return room_colors.get(room_type, self.colors['bg_card'])
        
    def add_room_visual_elements(self, room_frame, room_type):
        """Add visual elements that represent room type"""
        visual_frame = ctk.CTkFrame(room_frame, fg_color="transparent")
        visual_frame.pack(side="bottom", fill="x", padx=8, pady=(0, 8))
        
        if room_type == "storage":
            # Shelf lines for storage
            for i in range(3):
                shelf_line = ctk.CTkFrame(visual_frame, height=2, fg_color=self.colors['text_muted'])
                shelf_line.pack(fill="x", pady=1)
                
        elif room_type == "hall":
            # Chair row indicators for halls
            chairs_frame = ctk.CTkFrame(visual_frame, fg_color="transparent")
            chairs_frame.pack()
            
            for i in range(5):
                chair_dot = ctk.CTkLabel(chairs_frame, text="•", font=self.fonts['caption'], 
                                       text_color=self.colors['accent_green'])
                chair_dot.pack(side="left", padx=1)
                
        elif room_type == "conference":
            # Table indicator for conference rooms
            table_indicator = ctk.CTkFrame(visual_frame, height=8, width=40, 
                                         fg_color=self.colors['accent_blue'], corner_radius=4)
            table_indicator.pack()
            
        elif room_type == "lab":
            # Lab bench indicators
            bench_frame = ctk.CTkFrame(visual_frame, fg_color="transparent")
            bench_frame.pack()
            
            for i in range(2):
                bench = ctk.CTkFrame(bench_frame, height=4, width=15, 
                                   fg_color=self.colors['warning'], corner_radius=2)
                bench.pack(side="left", padx=2)
                
    def show_room_details(self, room_name):
        """Show detailed room information panel"""
        # Create overlay for room details
        details_overlay = ctk.CTkFrame(
            self.root,
            width=350,
            height=400,
            fg_color=self.colors['bg_secondary'],
            corner_radius=20,
            border_width=2,
            border_color=self.colors['glow']
        )
        details_overlay.place(x=20, y=200)
        
        # Room details header
        header_label = ctk.CTkLabel(
            details_overlay,
            text=f"📍 {room_name}",
            font=self.fonts['heading_medium'],
            text_color=self.colors['text_primary']
        )
        header_label.pack(pady=(20, 10))
        
        # Get room data
        room_data = self.zone_counts.get(room_name, {"total": 0})
        
        # Asset summary
        summary_frame = ctk.CTkFrame(details_overlay, fg_color=self.colors['bg_card'], corner_radius=12)
        summary_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(summary_frame, text=f"Total Assets: {room_data['total']}", 
                    font=self.fonts['body_large'], text_color=self.colors['accent_blue']).pack(pady=(15, 5))
        
        # Asset breakdown
        asset_details = [
            ("Chairs", room_data.get("chairs", 0), "🪑"),
            ("Tables", room_data.get("tables", 0), "🪑"), 
            ("Projectors", room_data.get("projectors", 0), "📽️"),
            ("Screens", room_data.get("tvs", 0), "📺")
        ]
        
        for asset_type, count, icon in asset_details:
            if count > 0:
                detail_frame = ctk.CTkFrame(summary_frame, fg_color="transparent")
                detail_frame.pack(fill="x", padx=15, pady=2)
                
                ctk.CTkLabel(detail_frame, text=f"{icon} {asset_type}: {count}", 
                           font=self.fonts['body_medium'], text_color=self.colors['text_secondary']).pack(side="left")
        
        # Recent activity
        ctk.CTkLabel(details_overlay, text="Recent Activity", 
                    font=self.fonts['heading_small'], text_color=self.colors['text_primary']).pack(pady=(15, 10))
        
        activity_frame = ctk.CTkFrame(details_overlay, fg_color=self.colors['bg_card'], corner_radius=12)
        activity_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        recent_activities = [
            "Chair batch moved in (2 min ago)",
            "Asset scan completed (1 hour ago)",
            "Table deployment finished (3 hours ago)"
        ]
        
        for activity in recent_activities:
            ctk.CTkLabel(activity_frame, text=f"• {activity}", 
                        font=self.fonts['body_small'], text_color=self.colors['text_muted']).pack(anchor="w", padx=15, pady=3)
        
        # Close button
        close_btn = ctk.CTkButton(
            details_overlay,
            text="✕ Close",
            height=40,
            font=self.fonts['body_medium'],
            fg_color=self.colors['accent_blue'],
            hover_color=self.colors['glow'],
            corner_radius=12,
            command=lambda: details_overlay.destroy()
        )
        close_btn.pack(pady=20)
            
    def build_placeholder_screen(self):
        """Build placeholder for other screens"""
        placeholder = ctk.CTkFrame(
            self.content_frame,
            height=400,
            fg_color="transparent"
        )
        placeholder.pack(fill="x", padx=20, pady=50)
        placeholder.pack_propagate(False)
        
        icon_map = {
            "Event Planner": "📅",
            "Asset 360": "📦", 
            "Alerts": "🔔",
            "Analytics": "📊"
        }
        
        icon = icon_map.get(self.current_screen, "⚡")
        
        placeholder_label = ctk.CTkLabel(
            placeholder,
            text=f"{icon}\n\n{self.current_screen}\n\nComing Soon...",
            font=self.fonts['heading_medium'],
            text_color=self.colors['text_muted'],
            justify="center"
        )
        placeholder_label.pack(expand=True)
        
    def create_kpi_card(self, parent, title, value, accent_color):
        """Create a KPI card"""
        card = ctk.CTkFrame(
            parent,
            height=100,
            fg_color=self.colors['bg_card'],
            corner_radius=12
        )
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=self.fonts['heading_medium'],
            text_color=accent_color
        )
        value_label.pack(pady=(20, 5))
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=self.fonts['body_small'],
            text_color=self.colors['text_secondary']
        )
        title_label.pack(pady=(0, 20))
        
        return card
        
    def create_quick_actions(self):
        """Create role-aware Quick Actions section"""
        role_config = self.role_configs.get(self.current_role, self.role_configs["Logistics"])
        
        actions_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        actions_frame.pack(fill="x", padx=20, pady=(0, 30))
        
        title_label = ctk.CTkLabel(
            actions_frame,
            text=f"{self.current_role} Actions",
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 15))
        
        # Get role-specific actions
        actions = role_config.get("quick_actions", [])
        
        for action in actions:
            action_btn = ctk.CTkButton(
                actions_frame,
                text=action,
                height=50,
                font=self.fonts['body_large'],
                fg_color=self.colors['bg_card'],
                text_color=self.colors['text_primary'],
                hover_color=role_config.get("theme_color", self.colors['accent_blue']),
                corner_radius=12,
                border_width=1,
                border_color=role_config.get("theme_color", self.colors['accent_blue']),
                command=lambda a=action: self.handle_quick_action(a)
            )
            action_btn.pack(fill="x", pady=(0, 10))
            
    def handle_quick_action(self, action):
        """Handle role-specific quick actions"""
        if "Deploy Event Setup" in action:
            self.navigate_to("Event Planner")
        elif "Generate Cost Report" in action:
            # Mock action for Finance role
            pass
        elif "Create Event" in action:
            self.navigate_to("Event Planner")
        # Add more action handlers as needed
            
    def create_live_activity(self):
        """Create Live Activity section"""
        activity_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        activity_frame.pack(fill="x", padx=20, pady=(0, 50))
        
        title_label = ctk.CTkLabel(
            activity_frame,
            text="Live Activity",
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 15))
        
        activities = [
            "25 chairs moved to Main Hall",
            "Projector Kit assigned to Conference Room",
            "Storage Room B scan completed"
        ]
        
        for activity in activities:
            activity_item = ctk.CTkFrame(
                activity_frame,
                height=60,
                fg_color=self.colors['bg_card'],
                corner_radius=12
            )
            activity_item.pack(fill="x", pady=(0, 10))
            activity_item.pack_propagate(False)
            
            dot_label = ctk.CTkLabel(
                activity_item,
                text="●",
                font=self.fonts['body_large'],
                text_color=self.colors['accent_green']
            )
            dot_label.pack(side="left", padx=(20, 10), pady=20)
            
            activity_label = ctk.CTkLabel(
                activity_item,
                text=activity,
                font=self.fonts['body_medium'],
                text_color=self.colors['text_primary'],
                anchor="w"
            )
            activity_label.pack(side="left", fill="x", expand=True, pady=20)
            
    def build_scanner(self):
        """Build the Asset Scanner & Registration screen"""
        # Scanner title
        title_container = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        title_container.pack(fill="x", padx=20, pady=(20, 20))
        
        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Scan RFID tags or QR codes to register or edit assets",
            font=self.fonts['body_large'],
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        subtitle_label.pack(fill="x")
        
        # Camera/Scanner preview
        scanner_container = ctk.CTkFrame(
            self.content_frame,
            height=200,
            fg_color=self.colors['bg_card'],
            corner_radius=16,
            border_width=2,
            border_color=self.colors['accent_blue']
        )
        scanner_container.pack(fill="x", padx=20, pady=(0, 20))
        scanner_container.pack_propagate(False)
        
        # Glowing scan frame
        scan_frame = ctk.CTkFrame(
            scanner_container,
            width=150,
            height=150,
            fg_color="transparent",
            border_width=3,
            border_color=self.colors['accent_green'],
            corner_radius=12
        )
        scan_frame.pack(expand=True, pady=20)
        
        scan_label = ctk.CTkLabel(
            scan_frame,
            text="📱\n\nPosition asset\nRFID tag or\nQR code here",
            font=self.fonts['body_medium'],
            text_color=self.colors['text_muted'],
            justify="center"
        )
        scan_label.pack(expand=True)
        
        # Simulate Scan button
        scan_btn = ctk.CTkButton(
            self.content_frame,
            text="🔍 Simulate Scan",
            height=50,
            font=self.fonts['body_large'],
            fg_color=self.colors['accent_blue'],
            hover_color=self.colors['bg_card'],
            corner_radius=12,
            command=self.simulate_scan
        )
        scan_btn.pack(fill="x", padx=20, pady=(0, 30))
        
        # Quick fill templates section
        templates_label = ctk.CTkLabel(
            self.content_frame,
            text="Quick Fill Templates",
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        templates_label.pack(fill="x", padx=20, pady=(0, 15))
        
        # Template buttons grid
        templates_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        templates_frame.pack(fill="x", padx=20, pady=(0, 30))
        
        templates = [
            ("Chair", "🪑"),
            ("Table", "🪑"), 
            ("Projector", "📽️"),
            ("Speaker", "🔊"),
            ("TV / Screen", "📺"),
            ("Laptop", "💻")
        ]
        
        for i, (name, icon) in enumerate(templates):
            row = i // 2
            col = i % 2
            
            template_btn = ctk.CTkButton(
                templates_frame,
                text=f"{icon} {name}",
                height=50,
                font=self.fonts['body_medium'],
                fg_color=self.colors['bg_card'],
                text_color=self.colors['text_primary'],
                hover_color=self.colors['bg_secondary'],
                corner_radius=12,
                border_width=1,
                border_color=self.colors['accent_green'],
                command=lambda asset_type=name: self.quick_fill_asset(asset_type)
            )
            template_btn.grid(row=row, column=col, padx=(0, 10 if col == 0 else 0),
                             pady=(0, 10), sticky="ew")
        
        templates_frame.grid_columnconfigure(0, weight=1)
        templates_frame.grid_columnconfigure(1, weight=1)
        
    def simulate_scan(self):
        """Simulate scanning an RFID tag or QR code"""
        import random
        
        # Simulate random scan results
        scan_types = [
            ("new", "RFID-CH-1042", "Chair"),
            ("existing", "RFID-TB-2210", "Table"), 
            ("new", "RFID-PR-031", "Projector"),
            ("existing", "RFID-SP-445", "Speaker"),
            ("new", "RFID-TV-789", "TV"),
        ]
        
        scan_type, asset_id, asset_type = random.choice(scan_types)
        
        if scan_type == "new":
            self.show_new_asset_form(asset_id, asset_type)
        else:
            self.show_existing_asset_form(asset_id, asset_type)
            
    def show_new_asset_form(self, asset_id, asset_type):
        """Show the new asset registration form"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Header
        header_label = ctk.CTkLabel(
            self.content_frame,
            text="🆕 New Asset Detected",
            font=self.fonts['heading_medium'],
            text_color=self.colors['success'],
        )
        header_label.pack(padx=20, pady=(20, 10))
        
        detected_label = ctk.CTkLabel(
            self.content_frame,
            text=f"Asset ID: {asset_id}",
            font=self.fonts['body_large'],
            text_color=self.colors['text_primary'],
        )
        detected_label.pack(padx=20, pady=(0, 30))
        
        # Registration form
        form_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=16
        )
        form_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Asset Type dropdown
        ctk.CTkLabel(form_frame, text="Asset Type", font=self.fonts['body_medium'], 
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(20, 5), anchor="w")
        
        asset_type_var = ctk.StringVar(value=asset_type)
        asset_type_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["Chair", "Table", "Projector", "Speaker", "TV / Screen", "Laptop", "Lab Equipment", "Other"],
            variable=asset_type_var,
            font=self.fonts['body_medium'],
            dropdown_font=self.fonts['body_medium']
        )
        asset_type_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        # Product Name
        ctk.CTkLabel(form_frame, text="Product Name", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(0, 5), anchor="w")
        
        product_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="e.g. Standard Event Chair",
            font=self.fonts['body_medium'],
            height=40
        )
        product_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Current Zone
        ctk.CTkLabel(form_frame, text="Current Zone", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(0, 5), anchor="w")
        
        zone_var = ctk.StringVar(value="Storage Room A")
        zone_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["Storage Room A", "Storage Room B", "Main Hall", "Conference Room", "Lab 4", "Loading Area", "Event Hall"],
            variable=zone_var,
            font=self.fonts['body_medium']
        )
        zone_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        # Condition
        ctk.CTkLabel(form_frame, text="Condition", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(0, 5), anchor="w")
        
        condition_var = ctk.StringVar(value="Good")
        condition_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["New", "Good", "Worn", "Damaged", "Needs Repair"],
            variable=condition_var,
            font=self.fonts['body_medium']
        )
        condition_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        # Status
        ctk.CTkLabel(form_frame, text="Status", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(0, 5), anchor="w")
        
        status_var = ctk.StringVar(value="Available")
        status_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["Available", "In Use", "In Transit", "Reserved", "Maintenance"],
            variable=status_var,
            font=self.fonts['body_medium']
        )
        status_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        # Department Owner
        ctk.CTkLabel(form_frame, text="Department Owner", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(0, 5), anchor="w")
        
        dept_var = ctk.StringVar(value="Logistics")
        dept_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["Logistics", "Events", "Facilities", "Finance", "Maintenance"],
            variable=dept_var,
            font=self.fonts['body_medium']
        )
        dept_menu.pack(fill="x", padx=20, pady=(0, 20))
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            height=50,
            font=self.fonts['body_large'],
            fg_color=self.colors['bg_card'],
            text_color=self.colors['text_primary'],
            hover_color=self.colors['bg_secondary'],
            corner_radius=12,
            command=lambda: self.navigate_to("Scanner")
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ Register Asset",
            height=50,
            font=self.fonts['body_large'],
            fg_color=self.colors['success'],
            hover_color=self.colors['accent_green'],
            corner_radius=12,
            command=lambda: self.save_new_asset(asset_id, asset_type_var.get(), 
                                               product_entry.get(), zone_var.get(),
                                               condition_var.get(), status_var.get(), dept_var.get())
        )
        save_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
    def show_existing_asset_form(self, asset_id, asset_type):
        """Show the existing asset editing form"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Header
        header_label = ctk.CTkLabel(
            self.content_frame,
            text="📋 Existing Asset Found",
            font=self.fonts['heading_medium'],
            text_color=self.colors['warning'],
        )
        header_label.pack(padx=20, pady=(20, 10))
        
        # Asset summary card
        summary_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=16
        )
        summary_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        summary_data = [
            ("Asset ID", asset_id),
            ("Product Name", f"Standard Event {asset_type}"),
            ("Type", asset_type),
            ("Current Zone", "Main Hall"),
            ("Condition", "Good"),
            ("Status", "In Use"),
            ("Last Updated", "2 hours ago")
        ]
        
        for label, value in summary_data:
            row_frame = ctk.CTkFrame(summary_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=2)
            
            ctk.CTkLabel(row_frame, text=f"{label}:", font=self.fonts['body_small'], 
                        text_color=self.colors['text_muted']).pack(side="left")
            ctk.CTkLabel(row_frame, text=value, font=self.fonts['body_medium'],
                        text_color=self.colors['text_primary']).pack(side="right")
        
        # Edit form
        edit_label = ctk.CTkLabel(
            self.content_frame,
            text="Update Asset Information",
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary']
        )
        edit_label.pack(padx=20, pady=(20, 10), anchor="w")
        
        edit_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=16
        )
        edit_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Editable fields
        ctk.CTkLabel(edit_frame, text="Condition", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(20, 5), anchor="w")
        
        edit_condition_var = ctk.StringVar(value="Good")
        edit_condition_menu = ctk.CTkOptionMenu(
            edit_frame,
            values=["New", "Good", "Worn", "Damaged", "Needs Repair"],
            variable=edit_condition_var,
            font=self.fonts['body_medium']
        )
        edit_condition_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(edit_frame, text="Zone", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(0, 5), anchor="w")
        
        edit_zone_var = ctk.StringVar(value="Main Hall")
        edit_zone_menu = ctk.CTkOptionMenu(
            edit_frame,
            values=["Storage Room A", "Storage Room B", "Main Hall", "Conference Room", "Lab 4", "Loading Area", "Event Hall"],
            variable=edit_zone_var,
            font=self.fonts['body_medium']
        )
        edit_zone_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(edit_frame, text="Status", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(0, 5), anchor="w")
        
        edit_status_var = ctk.StringVar(value="In Use")
        edit_status_menu = ctk.CTkOptionMenu(
            edit_frame,
            values=["Available", "In Use", "In Transit", "Reserved", "Maintenance"],
            variable=edit_status_var,
            font=self.fonts['body_medium']
        )
        edit_status_menu.pack(fill="x", padx=20, pady=(0, 20))
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            height=50,
            font=self.fonts['body_large'],
            fg_color=self.colors['bg_card'],
            text_color=self.colors['text_primary'],
            hover_color=self.colors['bg_secondary'],
            corner_radius=12,
            command=lambda: self.navigate_to("Scanner")
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        update_btn = ctk.CTkButton(
            buttons_frame,
            text="💾 Update Asset",
            height=50,
            font=self.fonts['body_large'],
            fg_color=self.colors['accent_blue'],
            hover_color=self.colors['glow'],
            corner_radius=12,
            command=lambda: self.save_existing_asset(asset_id, edit_condition_var.get(),
                                                   edit_zone_var.get(), edit_status_var.get())
        )
        update_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
    def quick_fill_asset(self, asset_type):
        """Quick fill asset template"""
        import random
        
        # Generate random asset ID
        prefixes = {"Chair": "CH", "Table": "TB", "Projector": "PR", "Speaker": "SP", 
                   "TV / Screen": "TV", "Laptop": "LP"}
        prefix = prefixes.get(asset_type, "AS")
        asset_id = f"RFID-{prefix}-{random.randint(1000, 9999)}"
        
        self.show_new_asset_form(asset_id, asset_type)
        
    def save_new_asset(self, asset_id, asset_type, product_name, zone, condition, status, department):
        """Save new asset registration to shared state"""
        # Get appropriate icon for asset type
        icon_map = {
            "Chair": "🪑",
            "Table": "🪑", 
            "Projector": "📽️",
            "Speaker": "🔊",
            "TV / Screen": "📺",
            "TV": "📺",
            "Laptop": "💻",
            "Lab Equipment": "🔬",
            "Other": "📦"
        }
        
        # Add to shared assets state
        self.assets[asset_id] = {
            "id": asset_id,
            "type": asset_type,
            "product_name": product_name or f"Standard Event {asset_type}",
            "zone": zone,
            "condition": condition,
            "status": status,
            "department": department,
            "icon": icon_map.get(asset_type, "📦"),
            "last_updated": "Just now"
        }
        
        # Update zone counts
        self.update_zone_counts()
        
        self.show_success_message(f"Asset {asset_id} registered successfully!", 
                                f"New {asset_type.lower()} added to {zone}")
        
    def save_existing_asset(self, asset_id, condition, zone, status):
        """Save existing asset updates to shared state"""
        # Update existing asset in shared state
        if asset_id in self.assets:
            self.assets[asset_id]["condition"] = condition
            self.assets[asset_id]["zone"] = zone
            self.assets[asset_id]["status"] = status
            self.assets[asset_id]["last_updated"] = "Just now"
        else:
            # Create mock existing asset for demo
            self.assets[asset_id] = {
                "id": asset_id,
                "type": "Chair",  # Mock type
                "product_name": "Standard Event Chair",
                "zone": zone,
                "condition": condition,
                "status": status,
                "department": "Logistics",
                "icon": "🪑",
                "last_updated": "Just now"
            }
        
        # Update zone counts
        self.update_zone_counts()
        
        self.show_success_message(f"Asset {asset_id} updated successfully!", 
                                f"Condition: {condition}, Zone: {zone}")
        
    def show_success_message(self, title, message):
        """Show success confirmation"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        success_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        success_frame.pack(expand=True, padx=20, pady=50)
        
        # Success icon and message
        success_label = ctk.CTkLabel(
            success_frame,
            text="✅",
            font=('SF Pro Display', 48, 'bold'),
            text_color=self.colors['success']
        )
        success_label.pack(pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            success_frame,
            text=title,
            font=self.fonts['heading_medium'],
            text_color=self.colors['text_primary'],
            justify="center"
        )
        title_label.pack(pady=(0, 10))
        
        message_label = ctk.CTkLabel(
            success_frame,
            text=message,
            font=self.fonts['body_large'],
            text_color=self.colors['text_secondary'],
            justify="center"
        )
        message_label.pack(pady=(0, 30))
        
        # Return to scanner button
        return_btn = ctk.CTkButton(
            success_frame,
            text="📱 Scan Another Asset",
            height=50,
            font=self.fonts['body_large'],
            fg_color=self.colors['accent_blue'],
            hover_color=self.colors['glow'],
            corner_radius=12,
            command=lambda: self.navigate_to("Scanner")
        )
        return_btn.pack()

    def build_event_planner(self):
        """Build the Event Planner & Deployment screen"""
        # Event planner title
        title_container = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        title_container.pack(fill="x", padx=20, pady=(20, 20))
        
        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Plan event deployments and coordinate asset movements",
            font=self.fonts['body_large'],
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        subtitle_label.pack(fill="x")
        
        # Event planning form
        form_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=16
        )
        form_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Form header
        form_header = ctk.CTkLabel(
            form_frame,
            text="📅 Event Details",
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary']
        )
        form_header.pack(pady=(20, 15))
        
        # Event Name
        ctk.CTkLabel(form_frame, text="Event Name", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(0, 5), anchor="w")
        
        self.event_name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="e.g. Annual Conference",
            font=self.fonts['body_medium'],
            height=40
        )
        self.event_name_entry.pack(fill="x", padx=20, pady=(0, 15))
        self.event_name_entry.insert(0, "Annual Conference")
        
        # Zone selection grid
        zones_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        zones_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # From Zone
        from_zone_frame = ctk.CTkFrame(zones_frame, fg_color="transparent")
        from_zone_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(from_zone_frame, text="From Zone", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(anchor="w", pady=(0, 5))
        
        self.from_zone_var = ctk.StringVar(value="Storage Room B")
        from_zone_menu = ctk.CTkOptionMenu(
            from_zone_frame,
            values=["Storage Room A", "Storage Room B", "Loading Area", "Event Hall"],
            variable=self.from_zone_var,
            font=self.fonts['body_medium']
        )
        from_zone_menu.pack(fill="x")
        
        # To Zone
        to_zone_frame = ctk.CTkFrame(zones_frame, fg_color="transparent")
        to_zone_frame.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(to_zone_frame, text="To Zone", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(anchor="w", pady=(0, 5))
        
        self.to_zone_var = ctk.StringVar(value="Main Hall")
        to_zone_menu = ctk.CTkOptionMenu(
            to_zone_frame,
            values=["Main Hall", "Conference Room", "Event Hall", "Lab 4"],
            variable=self.to_zone_var,
            font=self.fonts['body_medium']
        )
        to_zone_menu.pack(fill="x")
        
        # Asset requirements section
        assets_label = ctk.CTkLabel(
            form_frame,
            text="Asset Requirements",
            font=self.fonts['body_medium'],
            text_color=self.colors['text_primary']
        )
        assets_label.pack(padx=20, pady=(15, 10), anchor="w")
        
        # Asset requirements grid
        assets_grid = ctk.CTkFrame(form_frame, fg_color="transparent")
        assets_grid.pack(fill="x", padx=20, pady=(0, 15))
        
        # Asset input pairs
        assets_config = [
            ("Chairs", "100", "🪑"),
            ("Tables", "10", "🪑"),
            ("Projectors", "2", "📽️"),
            ("Speakers", "2", "🔊")
        ]
        
        self.asset_vars = {}
        for i, (asset_type, default_val, icon) in enumerate(assets_config):
            row = i // 2
            col = i % 2
            
            asset_frame = ctk.CTkFrame(assets_grid, fg_color="transparent")
            asset_frame.grid(row=row, column=col, padx=(0, 10 if col == 0 else 0),
                           pady=(0, 10), sticky="ew")
            
            # Asset label with icon
            label_frame = ctk.CTkFrame(asset_frame, fg_color="transparent")
            label_frame.pack(fill="x")
            
            ctk.CTkLabel(label_frame, text=f"{icon} {asset_type}", 
                        font=self.fonts['body_small'], text_color=self.colors['text_secondary']).pack(side="left")
            
            # Asset quantity entry
            self.asset_vars[asset_type.lower()] = ctk.StringVar(value=default_val)
            asset_entry = ctk.CTkEntry(
                asset_frame,
                textvariable=self.asset_vars[asset_type.lower()],
                width=80,
                height=35,
                font=self.fonts['body_medium']
            )
            asset_entry.pack(pady=(5, 0))
        
        assets_grid.grid_columnconfigure(0, weight=1)
        assets_grid.grid_columnconfigure(1, weight=1)
        
        # Return time
        ctk.CTkLabel(form_frame, text="Expected Return Time", font=self.fonts['body_medium'],
                    text_color=self.colors['text_primary']).pack(padx=20, pady=(10, 5), anchor="w")
        
        self.return_time_var = ctk.StringVar(value="6 hours")
        return_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["2 hours", "4 hours", "6 hours", "8 hours", "1 day", "2 days"],
            variable=self.return_time_var,
            font=self.fonts['body_medium']
        )
        return_menu.pack(fill="x", padx=20, pady=(0, 20))
        
        # Asset Assignment Section
        assignment_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=16
        )
        assignment_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Assignment section header
        assignment_header = ctk.CTkLabel(
            assignment_frame,
            text="📋 Assign Assets",
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary']
        )
        assignment_header.pack(pady=(20, 15))
        
        # Assignment mode selector
        mode_frame = ctk.CTkFrame(assignment_frame, fg_color="transparent")
        mode_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Initialize assignment mode if not set
        if not hasattr(self, 'assignment_mode'):
            self.assignment_mode = "bulk"
            self.assigned_assets = []
            self.asset_batches = []
        
        # Mode selector buttons
        bulk_btn = ctk.CTkButton(
            mode_frame,
            text="📦 Bulk Assign",
            height=40,
            font=self.fonts['body_medium'],
            fg_color=self.colors['accent_blue'] if self.assignment_mode == "bulk" else self.colors['bg_secondary'],
            text_color=self.colors['text_primary'],
            hover_color=self.colors['accent_blue'],
            corner_radius=12,
            command=lambda: self.switch_assignment_mode("bulk")
        )
        bulk_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        scan_btn = ctk.CTkButton(
            mode_frame,
            text="📱 Scan to Assign", 
            height=40,
            font=self.fonts['body_medium'],
            fg_color=self.colors['accent_blue'] if self.assignment_mode == "scan" else self.colors['bg_secondary'],
            text_color=self.colors['text_primary'],
            hover_color=self.colors['accent_blue'],
            corner_radius=12,
            command=lambda: self.switch_assignment_mode("scan")
        )
        scan_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # Assignment interface container
        self.assignment_interface = ctk.CTkFrame(assignment_frame, fg_color="transparent")
        self.assignment_interface.pack(fill="x", padx=20, pady=(0, 20))
        
        # Build the appropriate assignment interface
        self.build_assignment_interface()
        
        # Create Plan button
        create_plan_btn = ctk.CTkButton(
            self.content_frame,
            text="📊 Create Deployment Plan",
            height=50,
            font=self.fonts['body_large'],
            fg_color=self.colors['accent_blue'],
            hover_color=self.colors['glow'],
            corner_radius=12,
            command=self.create_deployment_plan
        )
        create_plan_btn.pack(fill="x", padx=20, pady=(0, 30))
        
    def switch_assignment_mode(self, mode):
        """Switch between bulk assign and scan to assign modes"""
        self.assignment_mode = mode
        self.build_assignment_interface()
        
    def build_assignment_interface(self):
        """Build the assignment interface based on current mode"""
        # Clear existing interface
        for widget in self.assignment_interface.winfo_children():
            widget.destroy()
            
        if self.assignment_mode == "bulk":
            self.build_bulk_assign_interface()
        else:
            self.build_scan_assign_interface()
            
    def build_bulk_assign_interface(self):
        """Build the bulk assignment interface"""
        # Storage zone selector
        zone_label = ctk.CTkLabel(
            self.assignment_interface,
            text="Select Source Zone",
            font=self.fonts['body_medium'],
            text_color=self.colors['text_primary']
        )
        zone_label.pack(anchor="w", pady=(0, 10))
        
        # Get available zones with stock
        available_zones = []
        for zone_name, zone_data in self.zone_counts.items():
            if zone_data["total"] > 0:
                available_zones.append(zone_name)
        
        if not hasattr(self, 'bulk_source_zone'):
            self.bulk_source_zone = available_zones[0] if available_zones else "Storage Room B"
        
        bulk_zone_var = ctk.StringVar(value=self.bulk_source_zone)
        zone_menu = ctk.CTkOptionMenu(
            self.assignment_interface,
            values=available_zones or ["Storage Room B"],
            variable=bulk_zone_var,
            font=self.fonts['body_medium'],
            command=lambda zone: setattr(self, 'bulk_source_zone', zone)
        )
        zone_menu.pack(fill="x", pady=(0, 15))
        
        # Zone stock display
        stock_frame = ctk.CTkFrame(
            self.assignment_interface,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12
        )
        stock_frame.pack(fill="x", pady=(0, 15))
        
        stock_header = ctk.CTkLabel(
            stock_frame,
            text="Available Stock",
            font=self.fonts['body_medium'],
            text_color=self.colors['accent_blue']
        )
        stock_header.pack(pady=(15, 10))
        
        # Get current zone data
        current_zone_data = self.zone_counts.get(self.bulk_source_zone, {})
        
        stock_items = [
            ("Chairs", current_zone_data.get("chairs", 0), "🪑"),
            ("Tables", current_zone_data.get("tables", 0), "🪑"),
            ("Projectors", current_zone_data.get("projectors", 0), "📽️"),
            ("Speakers", current_zone_data.get("speakers", 0), "🔊")
        ]
        
        for asset_name, available_count, icon in stock_items:
            if available_count > 0:
                stock_row = ctk.CTkFrame(stock_frame, fg_color="transparent")
                stock_row.pack(fill="x", padx=15, pady=2)
                
                ctk.CTkLabel(stock_row, text=f"{icon} {asset_name}",
                           font=self.fonts['body_medium'], text_color=self.colors['text_secondary']).pack(side="left")
                ctk.CTkLabel(stock_row, text=f"{available_count} available",
                           font=self.fonts['body_medium'], text_color=self.colors['success']).pack(side="right")
        
        stock_frame.pack_configure(pady=(0, 15))
        
        # Batch generation preview
        self.show_batch_preview()
        
        # Confirm bulk assignment button
        confirm_btn = ctk.CTkButton(
            self.assignment_interface,
            text="✅ Confirm Bulk Assignment",
            height=45,
            font=self.fonts['body_medium'],
            fg_color=self.colors['success'],
            hover_color=self.colors['accent_green'],
            corner_radius=12,
            command=self.confirm_bulk_assignment
        )
        confirm_btn.pack(fill="x", pady=(15, 0))
        
    def show_batch_preview(self):
        """Show auto-generated batch preview"""
        preview_frame = ctk.CTkFrame(
            self.assignment_interface,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12
        )
        preview_frame.pack(fill="x", pady=(0, 15))
        
        preview_header = ctk.CTkLabel(
            preview_frame,
            text="Generated Batches",
            font=self.fonts['body_medium'],
            text_color=self.colors['accent_green']
        )
        preview_header.pack(pady=(15, 10))
        
        # Generate batches based on requirements
        try:
            chairs_needed = int(self.asset_vars["chairs"].get()) if "chairs" in self.asset_vars else 0
            tables_needed = int(self.asset_vars["tables"].get()) if "tables" in self.asset_vars else 0
            projectors_needed = int(self.asset_vars["projectors"].get()) if "projectors" in self.asset_vars else 0
            speakers_needed = int(self.asset_vars["speakers"].get()) if "speakers" in self.asset_vars else 0
        except:
            chairs_needed = tables_needed = projectors_needed = speakers_needed = 0
        
        # Generate chair batches (25 per batch)
        if chairs_needed > 0:
            chair_batches = (chairs_needed + 24) // 25  # Round up
            for i in range(chair_batches):
                batch_size = min(25, chairs_needed - (i * 25))
                if batch_size > 0:
                    batch_row = ctk.CTkFrame(preview_frame, fg_color="transparent")
                    batch_row.pack(fill="x", padx=15, pady=2)
                    
                    ctk.CTkLabel(batch_row, text=f"🪑 Chair Batch {i+1}: {batch_size} units",
                               font=self.fonts['body_small'], text_color=self.colors['text_secondary']).pack(side="left")
        
        # Generate table batches (5 per batch)
        if tables_needed > 0:
            table_batches = (tables_needed + 4) // 5  # Round up
            for i in range(table_batches):
                batch_size = min(5, tables_needed - (i * 5))
                if batch_size > 0:
                    batch_row = ctk.CTkFrame(preview_frame, fg_color="transparent")
                    batch_row.pack(fill="x", padx=15, pady=2)
                    
                    ctk.CTkLabel(batch_row, text=f"🪑 Table Batch {i+1}: {batch_size} units",
                               font=self.fonts['body_small'], text_color=self.colors['text_secondary']).pack(side="left")
        
        # Projectors and speakers (individual items)
        if projectors_needed > 0:
            batch_row = ctk.CTkFrame(preview_frame, fg_color="transparent")
            batch_row.pack(fill="x", padx=15, pady=2)
            
            ctk.CTkLabel(batch_row, text=f"📽️ Projector Kit: {projectors_needed} units",
                       font=self.fonts['body_small'], text_color=self.colors['text_secondary']).pack(side="left")
        
        if speakers_needed > 0:
            batch_row = ctk.CTkFrame(preview_frame, fg_color="transparent")
            batch_row.pack(fill="x", padx=15, pady=2)
            
            ctk.CTkLabel(batch_row, text=f"🔊 Speaker Set: {speakers_needed} units",
                       font=self.fonts['body_small'], text_color=self.colors['text_secondary']).pack(side="left")
        
        # Readiness indicator
        current_zone_data = self.zone_counts.get(self.bulk_source_zone, {})
        chairs_available = current_zone_data.get("chairs", 0)
        tables_available = current_zone_data.get("tables", 0) 
        projectors_available = current_zone_data.get("projectors", 0)
        speakers_available = current_zone_data.get("speakers", 0)
        
        readiness_scores = []
        if chairs_needed > 0:
            readiness_scores.append(min(100, (chairs_available / chairs_needed) * 100))
        if tables_needed > 0:
            readiness_scores.append(min(100, (tables_available / tables_needed) * 100))
        if projectors_needed > 0:
            readiness_scores.append(min(100, (projectors_available / projectors_needed) * 100))
        if speakers_needed > 0:
            readiness_scores.append(min(100, (speakers_available / speakers_needed) * 100))
        
        readiness = sum(readiness_scores) // len(readiness_scores) if readiness_scores else 100
        readiness_color = self.colors['success'] if readiness >= 95 else \
                         self.colors['warning'] if readiness >= 80 else self.colors['error']
        
        readiness_row = ctk.CTkFrame(preview_frame, fg_color="transparent")
        readiness_row.pack(fill="x", padx=15, pady=(10, 15))
        
        ctk.CTkLabel(readiness_row, text="Readiness:",
                   font=self.fonts['body_medium'], text_color=self.colors['text_secondary']).pack(side="left")
        ctk.CTkLabel(readiness_row, text=f"{readiness}%",
                   font=self.fonts['body_medium'], text_color=readiness_color).pack(side="right")
        
    def build_scan_assign_interface(self):
        """Build the scan-to-assign interface"""
        # Scanner preview
        scanner_frame = ctk.CTkFrame(
            self.assignment_interface,
            height=150,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12,
            border_width=2,
            border_color=self.colors['accent_green']
        )
        scanner_frame.pack(fill="x", pady=(0, 15))
        scanner_frame.pack_propagate(False)
        
        scan_frame = ctk.CTkFrame(
            scanner_frame,
            width=100,
            height=100,
            fg_color="transparent",
            border_width=2,
            border_color=self.colors['accent_green'],
            corner_radius=8
        )
        scan_frame.pack(expand=True, pady=20)
        
        scan_label = ctk.CTkLabel(
            scan_frame,
            text="📱\nScan Asset",
            font=self.fonts['body_medium'],
            text_color=self.colors['text_muted'],
            justify="center"
        )
        scan_label.pack(expand=True)
        
        # Scan button
        scan_btn = ctk.CTkButton(
            self.assignment_interface,
            text="🔍 Simulate Asset Scan",
            height=45,
            font=self.fonts['body_medium'],
            fg_color=self.colors['accent_blue'],
            hover_color=self.colors['glow'],
            corner_radius=12,
            command=self.simulate_asset_scan
        )
        scan_btn.pack(fill="x", pady=(0, 15))
        
        # Scanned assets list
        self.show_scanned_assets_list()
        
        # Assignment progress
        self.show_assignment_progress()
        
    def simulate_asset_scan(self):
        """Simulate scanning an asset for assignment"""
        import random
        
        # Get required asset types
        required_types = []
        try:
            if int(self.asset_vars["chairs"].get()) > 0:
                required_types.extend(["Chair"] * 3)  # Higher probability
            if int(self.asset_vars["tables"].get()) > 0:
                required_types.extend(["Table"] * 2)
            if int(self.asset_vars["projectors"].get()) > 0:
                required_types.append("Projector")
            if int(self.asset_vars["speakers"].get()) > 0:
                required_types.append("Speaker")
        except:
            required_types = ["Chair", "Table", "Projector", "Speaker"]
        
        if not required_types:
            required_types = ["Chair"]
        
        # Generate random asset
        asset_type = random.choice(required_types)
        prefixes = {"Chair": "CH", "Table": "TB", "Projector": "PR", "Speaker": "SP"}
        asset_id = f"RFID-{prefixes.get(asset_type, 'AS')}-{random.randint(1000, 9999)}"
        
        # Create mock asset
        mock_asset = {
            "id": asset_id,
            "type": asset_type,
            "zone": self.from_zone_var.get(),
            "condition": random.choice(["Good", "Good", "Good", "Worn", "Damaged"]),
            "status": random.choice(["Available", "Available", "In Use"])
        }
        
        self.show_scanned_asset_dialog(mock_asset)
        
    def show_scanned_asset_dialog(self, asset):
        """Show scanned asset confirmation dialog"""
        # Create overlay dialog
        dialog_overlay = ctk.CTkFrame(
            self.root,
            width=350,
            height=300,
            fg_color=self.colors['bg_secondary'],
            corner_radius=16,
            border_width=2,
            border_color=self.colors['glow']
        )
        dialog_overlay.place(x=20, y=250)
        
        # Dialog header
        header_label = ctk.CTkLabel(
            dialog_overlay,
            text="📱 Asset Scanned",
            font=self.fonts['heading_small'],
            text_color=self.colors['accent_blue']
        )
        header_label.pack(pady=(20, 15))
        
        # Asset details
        details_frame = ctk.CTkFrame(dialog_overlay, fg_color=self.colors['bg_card'], corner_radius=12)
        details_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        asset_details = [
            ("Asset ID", asset["id"]),
            ("Type", asset["type"]),
            ("Zone", asset["zone"]),
            ("Condition", asset["condition"]),
            ("Status", asset["status"])
        ]
        
        for label, value in asset_details:
            detail_row = ctk.CTkFrame(details_frame, fg_color="transparent")
            detail_row.pack(fill="x", padx=15, pady=3)
            
            ctk.CTkLabel(detail_row, text=f"{label}:", font=self.fonts['body_small'],
                        text_color=self.colors['text_muted']).pack(side="left")
            
            # Color code based on condition/status
            value_color = self.colors['text_primary']
            if label == "Condition" and value in ["Damaged", "Needs Repair"]:
                value_color = self.colors['error']
            elif label == "Status" and value != "Available":
                value_color = self.colors['warning']
                
            ctk.CTkLabel(detail_row, text=value, font=self.fonts['body_medium'],
                        text_color=value_color).pack(side="right")
        
        # Validation warnings
        warnings = self.validate_asset_assignment(asset)
        if warnings:
            warning_frame = ctk.CTkFrame(dialog_overlay, fg_color=self.colors['bg_card'], corner_radius=8)
            warning_frame.pack(fill="x", padx=20, pady=(0, 15))
            
            for warning in warnings:
                ctk.CTkLabel(warning_frame, text=f"⚠️ {warning}",
                           font=self.fonts['body_small'], text_color=self.colors['warning']).pack(padx=10, pady=3)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(dialog_overlay, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            height=40,
            font=self.fonts['body_medium'],
            fg_color=self.colors['bg_card'],
            text_color=self.colors['text_primary'],
            hover_color=self.colors['bg_secondary'],
            corner_radius=8,
            command=lambda: dialog_overlay.destroy()
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        assign_btn = ctk.CTkButton(
            buttons_frame,
            text="Add to Deployment",
            height=40,
            font=self.fonts['body_medium'],
            fg_color=self.colors['success'],
            hover_color=self.colors['accent_green'],
            corner_radius=8,
            command=lambda: self.add_asset_to_deployment(asset, dialog_overlay)
        )
        assign_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
    def validate_asset_assignment(self, asset):
        """Validate asset for assignment and return warnings"""
        warnings = []
        
        # Check if asset type is needed
        required_types = []
        try:
            if int(self.asset_vars["chairs"].get()) > 0:
                required_types.append("Chair")
            if int(self.asset_vars["tables"].get()) > 0:
                required_types.append("Table")
            if int(self.asset_vars["projectors"].get()) > 0:
                required_types.append("Projector")
            if int(self.asset_vars["speakers"].get()) > 0:
                required_types.append("Speaker")
        except:
            pass
        
        if asset["type"] not in required_types:
            warnings.append("This asset type is not required for this event.")
        
        # Check condition
        if asset["condition"] in ["Damaged", "Needs Repair"]:
            warnings.append("Asset condition is damaged. Assign anyway?")
        
        # Check status
        if asset["status"] != "Available":
            warnings.append("Asset is not currently available.")
        
        # Check zone match
        if asset["zone"] != self.from_zone_var.get():
            warnings.append("Asset is not in selected source zone.")
        
        return warnings
        
    def add_asset_to_deployment(self, asset, dialog):
        """Add scanned asset to deployment assignment"""
        if not hasattr(self, 'assigned_assets'):
            self.assigned_assets = []
        
        self.assigned_assets.append(asset)
        dialog.destroy()
        
        # Rebuild the scan interface to show updated lists
        self.build_assignment_interface()
        
    def show_scanned_assets_list(self):
        """Show list of scanned assets"""
        if not hasattr(self, 'assigned_assets') or not self.assigned_assets:
            return
        
        list_frame = ctk.CTkFrame(
            self.assignment_interface,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12
        )
        list_frame.pack(fill="x", pady=(0, 15))
        
        list_header = ctk.CTkLabel(
            list_frame,
            text="Scanned Assets",
            font=self.fonts['body_medium'],
            text_color=self.colors['accent_blue']
        )
        list_header.pack(pady=(15, 10))
        
        for asset in self.assigned_assets[-5:]:  # Show last 5 assets
            asset_row = ctk.CTkFrame(list_frame, fg_color="transparent")
            asset_row.pack(fill="x", padx=15, pady=2)
            
            icons = {"Chair": "🪑", "Table": "🪑", "Projector": "📽️", "Speaker": "🔊"}
            icon = icons.get(asset["type"], "📦")
            
            ctk.CTkLabel(asset_row, text=f"{icon} {asset['id']} ({asset['type']})",
                       font=self.fonts['body_small'], text_color=self.colors['text_secondary']).pack(side="left")
        
        list_frame.pack_configure(pady=(0, 15))
        
    def show_assignment_progress(self):
        """Show assignment progress"""
        if not hasattr(self, 'assigned_assets'):
            return
            
        progress_frame = ctk.CTkFrame(
            self.assignment_interface,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12
        )
        progress_frame.pack(fill="x")
        
        progress_header = ctk.CTkLabel(
            progress_frame,
            text="Assignment Progress",
            font=self.fonts['body_medium'],
            text_color=self.colors['accent_green']
        )
        progress_header.pack(pady=(15, 10))
        
        # Count assigned assets by type
        assigned_counts = {"Chair": 0, "Table": 0, "Projector": 0, "Speaker": 0}
        for asset in self.assigned_assets:
            asset_type = asset["type"]
            if asset_type in assigned_counts:
                assigned_counts[asset_type] += 1
        
        # Show progress for each type
        try:
            required = {
                "Chair": int(self.asset_vars["chairs"].get()),
                "Table": int(self.asset_vars["tables"].get()),
                "Projector": int(self.asset_vars["projectors"].get()),
                "Speaker": int(self.asset_vars["speakers"].get())
            }
        except:
            required = {"Chair": 0, "Table": 0, "Projector": 0, "Speaker": 0}
        
        for asset_type, assigned in assigned_counts.items():
            needed = required.get(asset_type, 0)
            if needed > 0:
                progress_row = ctk.CTkFrame(progress_frame, fg_color="transparent")
                progress_row.pack(fill="x", padx=15, pady=2)
                
                icons = {"Chair": "🪑", "Table": "🪑", "Projector": "📽️", "Speaker": "🔊"}
                icon = icons.get(asset_type, "📦")
                
                progress_color = self.colors['success'] if assigned >= needed else self.colors['warning']
                
                ctk.CTkLabel(progress_row, text=f"{icon} {asset_type}s:",
                           font=self.fonts['body_small'], text_color=self.colors['text_secondary']).pack(side="left")
                ctk.CTkLabel(progress_row, text=f"{assigned}/{needed}",
                           font=self.fonts['body_medium'], text_color=progress_color).pack(side="right")
        
        progress_frame.pack_configure(pady=(0, 0))
        
    def confirm_bulk_assignment(self):
        """Confirm bulk asset assignment"""
        # Generate asset batches based on requirements
        self.asset_batches = []
        
        try:
            chairs_needed = int(self.asset_vars["chairs"].get())
            tables_needed = int(self.asset_vars["tables"].get()) 
            projectors_needed = int(self.asset_vars["projectors"].get())
            speakers_needed = int(self.asset_vars["speakers"].get())
        except:
            chairs_needed = tables_needed = projectors_needed = speakers_needed = 0
        
        # Create chair batches
        chairs_assigned = 0
        batch_id = 1
        while chairs_assigned < chairs_needed:
            batch_size = min(25, chairs_needed - chairs_assigned)
            self.asset_batches.append({
                "type": "Chair",
                "batch_id": f"Chair-Batch-{batch_id}",
                "size": batch_size,
                "source_zone": self.bulk_source_zone
            })
            chairs_assigned += batch_size
            batch_id += 1
        
        # Create table batches  
        tables_assigned = 0
        batch_id = 1
        while tables_assigned < tables_needed:
            batch_size = min(5, tables_needed - tables_assigned)
            self.asset_batches.append({
                "type": "Table",
                "batch_id": f"Table-Batch-{batch_id}",
                "size": batch_size,
                "source_zone": self.bulk_source_zone
            })
            tables_assigned += batch_size
            batch_id += 1
        
        # Add projectors and speakers
        if projectors_needed > 0:
            self.asset_batches.append({
                "type": "Projector",
                "batch_id": "Projector-Kit",
                "size": projectors_needed,
                "source_zone": self.bulk_source_zone
            })
        
        if speakers_needed > 0:
            self.asset_batches.append({
                "type": "Speaker", 
                "batch_id": "Speaker-Set",
                "size": speakers_needed,
                "source_zone": self.bulk_source_zone
            })
        
        # Show confirmation message
        confirmation_frame = ctk.CTkFrame(
            self.assignment_interface,
            fg_color=self.colors['success'],
            corner_radius=12
        )
        confirmation_frame.pack(fill="x", pady=(15, 0))
        
        ctk.CTkLabel(
            confirmation_frame,
            text=f"✅ Bulk assignment confirmed! {len(self.asset_batches)} batches created.",
            font=self.fonts['body_medium'],
            text_color=self.colors['bg_primary']
        ).pack(pady=15)
        
    def create_deployment_plan(self):
        """Generate and display deployment plan"""
        import random
        
        # Get form data
        event_name = self.event_name_entry.get() or "Annual Conference"
        from_zone = self.from_zone_var.get()
        to_zone = self.to_zone_var.get()
        
        # Get asset requirements
        required_assets = {}
        for asset_type in ["chairs", "tables", "projectors", "speakers"]:
            try:
                required_assets[asset_type] = int(self.asset_vars[asset_type].get())
            except:
                required_assets[asset_type] = 0
        
        # Mock availability check against zone counts
        source_zone_data = self.zone_counts.get(from_zone, {})
        available_assets = {
            "chairs": source_zone_data.get("chairs", 0),
            "tables": source_zone_data.get("tables", 0), 
            "projectors": source_zone_data.get("projectors", 0),
            "speakers": source_zone_data.get("speakers", 0)
        }
        
        # Calculate readiness and shortages
        readiness_scores = []
        shortages = []
        
        for asset_type, required in required_assets.items():
            if required > 0:
                available = available_assets.get(asset_type, 0)
                if available >= required:
                    readiness_scores.append(100)
                else:
                    shortage = required - available
                    readiness_scores.append((available / required) * 100)
                    shortages.append(f"{shortage} {asset_type} shortage")
        
        overall_readiness = sum(readiness_scores) // len(readiness_scores) if readiness_scores else 100
        
        # Generate deployment ID
        deployment_id = f"EV-{random.choice(['A', 'B', 'C'])}{random.randint(100, 999)}"
        
        # Create deployment object in shared state
        self.active_deployments[deployment_id] = {
            "id": deployment_id,
            "event_name": event_name,
            "from_zone": from_zone,
            "to_zone": to_zone,
            "required_assets": required_assets,
            "available_assets": available_assets,
            "readiness": overall_readiness,
            "shortages": shortages,
            "status": "Planned",
            "created": "Just now"
        }
        
        # Display deployment plan
        self.show_deployment_plan(deployment_id)
        
    def show_deployment_plan(self, deployment_id):
        """Display the generated deployment plan"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        deployment = self.active_deployments[deployment_id]
        role_config = self.role_configs.get(self.current_role, self.role_configs["Logistics"])
        
        # Plan header
        header_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 20))
        
        plan_icon = ctk.CTkLabel(
            header_frame,
            text="📋",
            font=('SF Pro Display', 32, 'bold'),
            text_color=role_config.get("theme_color", self.colors['accent_blue'])
        )
        plan_icon.pack()
        
        plan_title = ctk.CTkLabel(
            header_frame,
            text="Deployment Plan Created",
            font=self.fonts['heading_medium'],
            text_color=self.colors['text_primary']
        )
        plan_title.pack(pady=(10, 5))
        
        plan_subtitle = ctk.CTkLabel(
            header_frame,
            text=f"Deployment Group: {deployment_id}",
            font=self.fonts['body_large'],
            text_color=role_config.get("theme_color", self.colors['accent_blue'])
        )
        plan_subtitle.pack()
        
        # Event summary card
        summary_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=16,
            border_width=2,
            border_color=role_config.get("theme_color", self.colors['accent_blue'])
        )
        summary_card.pack(fill="x", padx=20, pady=(0, 20))
        
        # Event name and route
        event_header = ctk.CTkLabel(
            summary_card,
            text=deployment["event_name"],
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary']
        )
        event_header.pack(pady=(20, 10))
        
        route_label = ctk.CTkLabel(
            summary_card,
            text=f"{deployment['from_zone']} → {deployment['to_zone']}",
            font=self.fonts['body_large'],
            text_color=self.colors['text_secondary']
        )
        route_label.pack(pady=(0, 15))
        
        # Readiness indicator
        readiness = deployment["readiness"]
        readiness_color = self.colors['success'] if readiness >= 95 else \
                         self.colors['warning'] if readiness >= 80 else self.colors['error']
        
        readiness_frame = ctk.CTkFrame(summary_card, fg_color="transparent")
        readiness_frame.pack(pady=(0, 15))
        
        ctk.CTkLabel(readiness_frame, text="Readiness:", font=self.fonts['body_medium'],
                    text_color=self.colors['text_secondary']).pack(side="left", padx=(20, 10))
        ctk.CTkLabel(readiness_frame, text=f"{readiness}%", font=self.fonts['heading_small'],
                    text_color=readiness_color).pack(side="left")
        
        # Asset availability breakdown
        assets_label = ctk.CTkLabel(
            summary_card,
            text="Asset Availability",
            font=self.fonts['body_medium'],
            text_color=self.colors['text_primary']
        )
        assets_label.pack(padx=20, pady=(10, 10), anchor="w")
        
        for asset_type, required in deployment["required_assets"].items():
            if required > 0:
                available = deployment["available_assets"].get(asset_type, 0)
                
                asset_row = ctk.CTkFrame(summary_card, fg_color="transparent")
                asset_row.pack(fill="x", padx=20, pady=2)
                
                # Asset icon and name
                icons = {"chairs": "🪑", "tables": "🪑", "projectors": "📽️", "speakers": "🔊"}
                asset_info = ctk.CTkLabel(
                    asset_row,
                    text=f"{icons.get(asset_type, '📦')} {asset_type.title()}",
                    font=self.fonts['body_medium'],
                    text_color=self.colors['text_secondary']
                )
                asset_info.pack(side="left")
                
                # Availability status
                availability_color = self.colors['success'] if available >= required else self.colors['warning']
                availability_text = f"{available}/{required}"
                
                availability_label = ctk.CTkLabel(
                    asset_row,
                    text=availability_text,
                    font=self.fonts['body_medium'],
                    text_color=availability_color
                )
                availability_label.pack(side="right")
        
        # Warnings section
        if deployment["shortages"]:
            warnings_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color=self.colors['bg_card'],
                corner_radius=12,
                border_width=1,
                border_color=self.colors['warning']
            )
            warnings_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            warning_header = ctk.CTkLabel(
                warnings_frame,
                text="⚠️ Warnings",
                font=self.fonts['body_medium'],
                text_color=self.colors['warning']
            )
            warning_header.pack(pady=(15, 10))
            
            for shortage in deployment["shortages"]:
                warning_item = ctk.CTkLabel(
                    warnings_frame,
                    text=f"• {shortage} detected",
                    font=self.fonts['body_small'],
                    text_color=self.colors['text_muted']
                )
                warning_item.pack(padx=20, pady=2, anchor="w")
            
            warnings_frame.pack_configure(pady=(0, 20))
        
        # Role-specific details
        self.show_role_specific_deployment_details(summary_card, deployment)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        back_btn = ctk.CTkButton(
            buttons_frame,
            text="← Back to Planning",
            height=50,
            font=self.fonts['body_large'],
            fg_color=self.colors['bg_card'],
            text_color=self.colors['text_primary'],
            hover_color=self.colors['bg_secondary'],
            corner_radius=12,
            command=lambda: self.navigate_to("Event Planner")
        )
        back_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        start_btn = ctk.CTkButton(
            buttons_frame,
            text="🚀 Start Deployment",
            height=50,
            font=self.fonts['body_large'],
            fg_color=self.colors['success'],
            hover_color=self.colors['accent_green'],
            corner_radius=12,
            command=lambda: self.start_deployment(deployment_id)
        )
        start_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
    def show_role_specific_deployment_details(self, parent, deployment):
        """Show role-specific deployment information"""
        role_config = self.role_configs.get(self.current_role, self.role_configs["Logistics"])
        
        # Role-specific insights
        details_frame = ctk.CTkFrame(parent, fg_color="transparent")
        details_frame.pack(fill="x", padx=20, pady=(15, 20))
        
        role_title = ctk.CTkLabel(
            details_frame,
            text=f"{self.current_role} Details",
            font=self.fonts['body_medium'],
            text_color=role_config.get("theme_color", self.colors['accent_blue'])
        )
        role_title.pack(anchor="w", pady=(0, 10))
        
        if self.current_role == "Logistics":
            details = [
                "Movement route verified",
                f"Source stock: {deployment['from_zone']}",
                f"Destination capacity: {deployment['to_zone']}",
                "Transport coordination required"
            ]
        elif self.current_role == "Finance":
            total_assets = sum(deployment["required_assets"].values())
            estimated_value = total_assets * 150  # Mock calculation
            details = [
                f"Estimated deployed value: ${estimated_value:,}",
                "Cost center: Events",
                "Insurance coverage active",
                "Utilization tracking enabled"
            ]
        elif self.current_role == "Events":
            readiness = deployment["readiness"]
            details = [
                f"Setup readiness: {readiness}%",
                f"Event timeline: {deployment['event_name']}",
                "Return deadline: 6 hours",
                "Setup crew notification sent"
            ]
        else:
            details = ["Deployment plan ready"]
        
        for detail in details:
            detail_label = ctk.CTkLabel(
                details_frame,
                text=f"• {detail}",
                font=self.fonts['body_small'],
                text_color=self.colors['text_muted']
            )
            detail_label.pack(anchor="w", pady=1)
            
    def start_deployment(self, deployment_id):
        """Start the deployment process and show live movement visualizer"""
        if deployment_id in self.active_deployments:
            deployment = self.active_deployments[deployment_id]
            deployment["status"] = "In Transit"
            deployment["start_time"] = "Just now"
            
            # Initialize movement state
            self.init_deployment_movement(deployment_id)
            
            # Show live movement visualizer
            self.show_live_movement_screen(deployment_id)
            
    def init_deployment_movement(self, deployment_id):
        """Initialize deployment movement state"""
        deployment = self.active_deployments[deployment_id]
        
        # Create movement batches based on assignment mode
        if hasattr(self, 'asset_batches') and self.asset_batches:
            # Use existing batches from bulk assignment
            movement_batches = []
            for batch in self.asset_batches:
                movement_batches.append({
                    "id": batch["batch_id"],
                    "type": batch["type"],
                    "size": batch["size"],
                    "progress": 0.0,  # 0.0 = source, 1.0 = destination
                    "status": "preparing",  # preparing -> moving -> arrived
                    "eta": "2 min"
                })
        else:
            # Create batches from required assets for scan assignment or default
            movement_batches = []
            batch_id = 1
            
            for asset_type, required in deployment["required_assets"].items():
                if required > 0:
                    if asset_type == "chairs":
                        # 25 chairs per batch
                        chairs_remaining = required
                        while chairs_remaining > 0:
                            batch_size = min(25, chairs_remaining)
                            movement_batches.append({
                                "id": f"Chair-Batch-{batch_id}",
                                "type": "Chair",
                                "size": batch_size,
                                "progress": 0.0,
                                "status": "preparing",
                                "eta": f"{batch_id + 1} min"
                            })
                            chairs_remaining -= batch_size
                            batch_id += 1
                    
                    elif asset_type == "tables":
                        # 5 tables per batch
                        tables_remaining = required
                        table_batch_id = 1
                        while tables_remaining > 0:
                            batch_size = min(5, tables_remaining)
                            movement_batches.append({
                                "id": f"Table-Batch-{table_batch_id}",
                                "type": "Table", 
                                "size": batch_size,
                                "progress": 0.0,
                                "status": "preparing",
                                "eta": f"{len(movement_batches) + 2} min"
                            })
                            tables_remaining -= batch_size
                            table_batch_id += 1
                    
                    elif asset_type == "projectors":
                        movement_batches.append({
                            "id": "Projector-Kit",
                            "type": "Projector",
                            "size": required,
                            "progress": 0.0,
                            "status": "preparing",
                            "eta": f"{len(movement_batches) + 1} min"
                        })
                    
                    elif asset_type == "speakers":
                        movement_batches.append({
                            "id": "Speaker-Set",
                            "type": "Speaker",
                            "size": required,
                            "progress": 0.0,
                            "status": "preparing", 
                            "eta": f"{len(movement_batches) + 1} min"
                        })
        
        # Store movement state
        deployment["movement_batches"] = movement_batches
        deployment["overall_progress"] = 0.0
        deployment["timeline"] = [
            f"Deployment {deployment_id} started",
            f"Preparing {len(movement_batches)} asset batches for movement"
        ]
        
    def show_live_movement_screen(self, deployment_id):
        """Show the live movement visualizer screen"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        deployment = self.active_deployments[deployment_id]
        role_config = self.role_configs.get(self.current_role, self.role_configs["Logistics"])
        
        # Movement screen header
        header_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        # Live deployment icon
        live_icon = ctk.CTkLabel(
            header_frame,
            text="🚛",
            font=('SF Pro Display', 28, 'bold'),
            text_color=self.colors['accent_green']
        )
        live_icon.pack()
        
        # Event name and deployment ID
        event_title = ctk.CTkLabel(
            header_frame,
            text=f"{deployment['event_name']} Setup",
            font=self.fonts['heading_medium'],
            text_color=self.colors['text_primary']
        )
        event_title.pack(pady=(5, 0))
        
        deployment_subtitle = ctk.CTkLabel(
            header_frame,
            text=f"Deployment {deployment_id}",
            font=self.fonts['body_large'],
            text_color=role_config.get("theme_color", self.colors['accent_blue'])
        )
        deployment_subtitle.pack(pady=(5, 0))
        
        # Route display
        route_frame = ctk.CTkFrame(
            self.content_frame,
            height=60,
            fg_color=self.colors['bg_card'],
            corner_radius=16,
            border_width=2,
            border_color=self.colors['accent_green']
        )
        route_frame.pack(fill="x", padx=20, pady=(0, 20))
        route_frame.pack_propagate(False)
        
        route_container = ctk.CTkFrame(route_frame, fg_color="transparent")
        route_container.pack(expand=True, pady=15)
        
        # From zone
        from_label = ctk.CTkLabel(
            route_container,
            text=deployment["from_zone"],
            font=self.fonts['body_medium'],
            text_color=self.colors['text_primary']
        )
        from_label.pack(side="left", padx=(20, 15))
        
        # Route arrow
        arrow_label = ctk.CTkLabel(
            route_container,
            text="🔄 →",
            font=self.fonts['body_large'],
            text_color=self.colors['accent_green']
        )
        arrow_label.pack(side="left", padx=10)
        
        # To zone
        to_label = ctk.CTkLabel(
            route_container,
            text=deployment["to_zone"],
            font=self.fonts['body_medium'],
            text_color=self.colors['text_primary']
        )
        to_label.pack(side="left", padx=(15, 20))
        
        # Live progress section
        progress_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=16
        )
        progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Overall progress
        progress_header = ctk.CTkLabel(
            progress_frame,
            text="Movement Progress",
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary']
        )
        progress_header.pack(pady=(20, 10))
        
        # Progress bar container
        progress_container = ctk.CTkFrame(progress_frame, fg_color="transparent")
        progress_container.pack(fill="x", padx=20, pady=(0, 15))
        
        overall_progress = deployment.get("overall_progress", 0)
        
        ctk.CTkLabel(progress_container, text="Overall:",
                    font=self.fonts['body_medium'], text_color=self.colors['text_secondary']).pack(side="left")
        ctk.CTkLabel(progress_container, text=f"{int(overall_progress * 100)}%",
                    font=self.fonts['body_large'], text_color=self.colors['success']).pack(side="right")
        
        # Moving batches section
        self.create_moving_batches_display(progress_frame, deployment)
        
        # Role-specific deployment view
        self.create_role_specific_movement_view(deployment)
        
        # Timeline feed
        self.create_timeline_feed(deployment)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Simulate movement button (for demo)
        simulate_btn = ctk.CTkButton(
            buttons_frame,
            text="⚡ Simulate Movement",
            height=50,
            font=self.fonts['body_medium'],
            fg_color=self.colors['accent_green'],
            hover_color=self.colors['success'],
            corner_radius=12,
            command=lambda: self.simulate_batch_movement(deployment_id)
        )
        simulate_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # View Live Map button
        map_btn = ctk.CTkButton(
            buttons_frame,
            text="View Live Map",
            height=50,
            font=self.fonts['body_medium'],
            fg_color=self.colors['accent_blue'],
            hover_color=self.colors['glow'],
            corner_radius=12,
            command=lambda: self.navigate_to("Live Map")
        )
        map_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
    def create_moving_batches_display(self, parent, deployment):
        """Create the moving batches visualization"""
        batches_label = ctk.CTkLabel(
            parent,
            text="Asset Batches",
            font=self.fonts['body_medium'],
            text_color=self.colors['text_primary']
        )
        batches_label.pack(padx=20, pady=(10, 10), anchor="w")
        
        # Show each batch with progress
        movement_batches = deployment.get("movement_batches", [])
        
        for batch in movement_batches[:6]:  # Show max 6 batches
            batch_frame = ctk.CTkFrame(
                parent,
                height=50,
                fg_color=self.colors['bg_secondary'],
                corner_radius=12
            )
            batch_frame.pack(fill="x", padx=20, pady=(0, 8))
            batch_frame.pack_propagate(False)
            
            # Batch info
            batch_container = ctk.CTkFrame(batch_frame, fg_color="transparent")
            batch_container.pack(fill="both", expand=True, padx=15, pady=12)
            
            # Batch icon and name
            icons = {"Chair": "🪑", "Table": "🪑", "Projector": "📽️", "Speaker": "🔊"}
            batch_icon = icons.get(batch["type"], "📦")
            
            batch_info = ctk.CTkLabel(
                batch_container,
                text=f"{batch_icon} {batch['id']} ({batch['size']} units)",
                font=self.fonts['body_small'],
                text_color=self.colors['text_secondary']
            )
            batch_info.pack(side="left")
            
            # Batch status and progress
            progress = batch.get("progress", 0)
            status = batch.get("status", "preparing")
            
            if status == "preparing":
                status_text = "Preparing"
                status_color = self.colors['warning']
            elif status == "moving":
                status_text = f"Moving ({int(progress * 100)}%)"
                status_color = self.colors['accent_blue']
            else:  # arrived
                status_text = "Arrived ✓"
                status_color = self.colors['success']
                
            batch_status = ctk.CTkLabel(
                batch_container,
                text=status_text,
                font=self.fonts['body_small'],
                text_color=status_color
            )
            batch_status.pack(side="right")
        
        if len(movement_batches) > 6:
            more_label = ctk.CTkLabel(
                parent,
                text=f"+ {len(movement_batches) - 6} more batches...",
                font=self.fonts['body_small'],
                text_color=self.colors['text_muted']
            )
            more_label.pack(padx=20, pady=(0, 20))
        else:
            # Add some padding
            ctk.CTkFrame(parent, height=20, fg_color="transparent").pack()
            
    def create_role_specific_movement_view(self, deployment):
        """Create role-specific movement information"""
        role_config = self.role_configs.get(self.current_role, self.role_configs["Logistics"])
        
        role_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=16,
            border_width=1,
            border_color=role_config.get("theme_color", self.colors['accent_blue'])
        )
        role_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        role_header = ctk.CTkLabel(
            role_frame,
            text=f"{self.current_role} View",
            font=self.fonts['heading_small'],
            text_color=role_config.get("theme_color", self.colors['accent_blue'])
        )
        role_header.pack(pady=(20, 15))
        
        if self.current_role == "Logistics":
            metrics = [
                ("Route Status", "Active"),
                ("Movement Progress", f"{int(deployment.get('overall_progress', 0) * 100)}%"),
                ("Batches In Transit", f"{len([b for b in deployment.get('movement_batches', []) if b.get('status') == 'moving'])}")
            ]
        elif self.current_role == "Finance":
            total_assets = sum(deployment["required_assets"].values())
            deployed_value = total_assets * 150
            metrics = [
                ("Deployed Asset Value", f"${deployed_value:,}"),
                ("Cost Center", "Events Department"),
                ("Insurance Coverage", "Active")
            ]
        else:  # Events
            readiness = deployment.get("readiness", 0)
            metrics = [
                ("Setup Readiness", f"{readiness}%"),
                ("Event Timeline", deployment["event_name"]),
                ("Arrival Progress", f"{int(deployment.get('overall_progress', 0) * 100)}%")
            ]
        
        for label, value in metrics:
            metric_row = ctk.CTkFrame(role_frame, fg_color="transparent")
            metric_row.pack(fill="x", padx=20, pady=3)
            
            ctk.CTkLabel(metric_row, text=f"{label}:",
                        font=self.fonts['body_small'], text_color=self.colors['text_secondary']).pack(side="left")
            ctk.CTkLabel(metric_row, text=value,
                        font=self.fonts['body_medium'], text_color=self.colors['text_primary']).pack(side="right")
        
        role_frame.pack_configure(pady=(0, 20))
        
    def create_timeline_feed(self, deployment):
        """Create live timeline feed"""
        timeline_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors['bg_card'],
            corner_radius=16
        )
        timeline_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        timeline_header = ctk.CTkLabel(
            timeline_frame,
            text="📋 Live Timeline",
            font=self.fonts['heading_small'],
            text_color=self.colors['text_primary']
        )
        timeline_header.pack(pady=(20, 15))
        
        timeline_events = deployment.get("timeline", [])
        
        for event in timeline_events[-4:]:  # Show last 4 events
            event_frame = ctk.CTkFrame(timeline_frame, fg_color="transparent")
            event_frame.pack(fill="x", padx=20, pady=3)
            
            # Timeline dot
            dot_label = ctk.CTkLabel(
                event_frame,
                text="●",
                font=self.fonts['body_medium'],
                text_color=self.colors['accent_green']
            )
            dot_label.pack(side="left", padx=(0, 15))
            
            # Timeline event
            event_label = ctk.CTkLabel(
                event_frame,
                text=event,
                font=self.fonts['body_small'],
                text_color=self.colors['text_secondary'],
                anchor="w"
            )
            event_label.pack(side="left", fill="x", expand=True)
        
        timeline_frame.pack_configure(pady=(0, 20))
        
    def simulate_batch_movement(self, deployment_id):
        """Simulate batch movement for demo purposes"""
        import random
        
        if deployment_id not in self.active_deployments:
            return
            
        deployment = self.active_deployments[deployment_id]
        movement_batches = deployment.get("movement_batches", [])
        
        # Find next batch to move
        for batch in movement_batches:
            if batch["status"] == "preparing":
                batch["status"] = "moving"
                batch["progress"] = 0.1
                deployment["timeline"].append(f"{batch['id']} left {deployment['from_zone']}")
                break
            elif batch["status"] == "moving" and batch["progress"] < 1.0:
                # Advance progress
                batch["progress"] = min(1.0, batch["progress"] + random.uniform(0.2, 0.4))
                if batch["progress"] >= 1.0:
                    batch["status"] = "arrived"
                    batch["progress"] = 1.0
                    deployment["timeline"].append(f"{batch['id']} arrived at {deployment['to_zone']}")
                    
                    # Update zone counts
                    self.update_zone_counts_for_batch(batch, deployment["from_zone"], deployment["to_zone"])
                break
        
        # Calculate overall progress
        total_batches = len(movement_batches)
        completed_batches = len([b for b in movement_batches if b["status"] == "arrived"])
        deployment["overall_progress"] = completed_batches / total_batches if total_batches > 0 else 0
        
        # Check if deployment is complete
        if deployment["overall_progress"] >= 1.0:
            deployment["status"] = "Deployed"
            deployment["timeline"].append(f"Deployment {deployment_id} completed successfully!")
            self.show_deployment_completion(deployment_id)
        else:
            # Refresh the movement screen
            self.show_live_movement_screen(deployment_id)
            
    def update_zone_counts_for_batch(self, batch, from_zone, to_zone):
        """Update zone counts when batch arrives"""
        batch_type = batch["type"].lower()
        batch_size = batch["size"]
        
        # Decrease from source zone
        if from_zone in self.zone_counts:
            if "chair" in batch_type and self.zone_counts[from_zone]["chairs"] >= batch_size:
                self.zone_counts[from_zone]["chairs"] -= batch_size
                self.zone_counts[from_zone]["total"] -= batch_size
        
        # Increase in destination zone
        if to_zone in self.zone_counts:
            if "chair" in batch_type:
                self.zone_counts[to_zone]["chairs"] += batch_size
                self.zone_counts[to_zone]["total"] += batch_size
            elif "table" in batch_type:
                self.zone_counts[to_zone]["tables"] += batch_size
                self.zone_counts[to_zone]["total"] += batch_size
            elif "projector" in batch_type:
                self.zone_counts[to_zone]["projectors"] += batch_size
                self.zone_counts[to_zone]["total"] += batch_size
            elif "speaker" in batch_type:
                self.zone_counts[to_zone]["speakers"] += batch_size
                self.zone_counts[to_zone]["total"] += batch_size
                
    def show_deployment_completion(self, deployment_id):
        """Show deployment completion screen"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        deployment = self.active_deployments[deployment_id]
        
        completion_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        completion_frame.pack(expand=True, padx=20, pady=50)
        
        # Success celebration
        success_icon = ctk.CTkLabel(
            completion_frame,
            text="🎉",
            font=('SF Pro Display', 48, 'bold'),
            text_color=self.colors['success']
        )
        success_icon.pack(pady=(0, 20))
        
        success_title = ctk.CTkLabel(
            completion_frame,
            text="Deployment Complete!",
            font=self.fonts['heading_medium'],
            text_color=self.colors['text_primary']
        )
        success_title.pack(pady=(0, 10))
        
        success_message = ctk.CTkLabel(
            completion_frame,
            text=f"{deployment['event_name']} setup completed successfully.\nAll assets delivered to {deployment['to_zone']}.",
            font=self.fonts['body_large'],
            text_color=self.colors['text_secondary'],
            justify="center"
        )
        success_message.pack(pady=(0, 30))
        
        # Next actions
        actions_frame = ctk.CTkFrame(completion_frame, fg_color="transparent")
        actions_frame.pack()
        
        map_btn = ctk.CTkButton(
            actions_frame,
            text="🗺️ View Live Map",
            height=45,
            font=self.fonts['body_medium'],
            fg_color=self.colors['accent_blue'],
            hover_color=self.colors['glow'],
            corner_radius=12,
            command=lambda: self.navigate_to("Live Map")
        )
        map_btn.pack(side="left", padx=(0, 10))
        
        home_btn = ctk.CTkButton(
            actions_frame,
            text="🏠 Command Center",
            height=45,
            font=self.fonts['body_medium'],
            fg_color=self.colors['bg_card'],
            text_color=self.colors['text_primary'],
            hover_color=self.colors['bg_secondary'],
            corner_radius=12,
            command=lambda: self.navigate_to("Command Center")
        )
        home_btn.pack(side="left")

    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = RELAYApp()
    app.run()

if __name__ == "__main__":
    main()
