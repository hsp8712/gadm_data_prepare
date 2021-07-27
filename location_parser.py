import geopandas
import pandas

pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', 1000)


ALL_COUNTRIES = [
    ('AFG', 'Afghanistan', 3),
    ('XAD', 'Akrotiri and Dhekelia', 2),
    ('ALA', 'Ã\x85land', 2),
    ('ALB', 'Albania', 4),
    ('DZA', 'Algeria', 3),
    ('ASM', 'American Samoa', 4),
    ('AND', 'Andorra', 2),
    ('AGO', 'Angola', 4),
    ('AIA', 'Anguilla', 1),
    ('ATA', 'Antarctica', 1),
    ('ATG', 'Antigua and Barbuda', 2),
    ('ARG', 'Argentina', 3),
    ('ARM', 'Armenia', 2),
    ('ABW', 'Aruba', 1),
    ('AUS', 'Australia', 3),
    ('AUT', 'Austria', 4),
    ('AZE', 'Azerbaijan', 3),
    ('BHS', 'Bahamas', 2),
    ('BHR', 'Bahrain', 2),
    ('BGD', 'Bangladesh', 5),
    ('BRB', 'Barbados', 2),
    ('BLR', 'Belarus', 3),
    ('BEL', 'Belgium', 5),
    ('BLZ', 'Belize', 2),
    ('BEN', 'Benin', 3),
    ('BMU', 'Bermuda', 2),
    ('BTN', 'Bhutan', 3),
    ('BOL', 'Bolivia', 4),
    ('BES', 'Bonaire, Saint Eustatius and Saba', 2),
    ('BIH', 'Bosnia and Herzegovina', 4),
    ('BWA', 'Botswana', 3),
    ('BVT', 'Bouvet Island', 1),
    ('BRA', 'Brazil', 4),
    ('IOT', 'British Indian Ocean Territory', 1),
    ('VGB', 'British Virgin Islands', 2),
    ('BRN', 'Brunei', 3),
    ('BGR', 'Bulgaria', 3),
    ('BFA', 'Burkina Faso', 4),
    ('BDI', 'Burundi', 5),
    ('KHM', 'Cambodia', 5),
    ('CMR', 'Cameroon', 4),
    ('CAN', 'Canada', 4),
    ('CPV', 'Cape Verde', 2),
    ('XCA', 'Caspian Sea', 1),
    ('CYM', 'Cayman Islands', 2),
    ('CAF', 'Central African Republic', 3),
    ('TCD', 'Chad', 4),
    ('CHL', 'Chile', 4),
    ('CHN', 'China', 4),
    ('CXR', 'Christmas Island', 1),
    ('XCL', 'Clipperton Island', 1),
    ('CCK', 'Cocos Islands', 1),
    ('COL', 'Colombia', 3),
    ('COM', 'Comoros', 2),
    ('COK', 'Cook Islands', 1),
    ('CRI', 'Costa Rica', 3),
    ('CIV', "CÃ´te d'Ivoire", 5),
    ('HRV', 'Croatia', 3),
    ('CUB', 'Cuba', 3),
    ('CUW', 'CuraÃ§ao', 1),
    ('CYP', 'Cyprus', 2),
    ('CZE', 'Czech Republic', 3),
    ('COD', 'Democratic Republic of the Congo', 4),
    ('DNK', 'Denmark', 3),
    ('DJI', 'Djibouti', 3),
    ('DMA', 'Dominica', 2),
    ('DOM', 'Dominican Republic', 3),
    ('TLS', 'East Timor', 4),
    ('ECU', 'Ecuador', 4),
    ('EGY', 'Egypt', 3),
    ('SLV', 'El Salvador', 3),
    ('GNQ', 'Equatorial Guinea', 3),
    ('ERI', 'Eritrea', 3),
    ('EST', 'Estonia', 4),
    ('ETH', 'Ethiopia', 4),
    ('FLK', 'Falkland Islands', 1),
    ('FRO', 'Faroe Islands', 3),
    ('FJI', 'Fiji', 3),
    ('FIN', 'Finland', 5),
    ('FRA', 'France', 6),
    ('GUF', 'French Guiana', 3),
    ('PYF', 'French Polynesia', 2),
    ('ATF', 'French Southern Territories', 2),
    ('GAB', 'Gabon', 3),
    ('GMB', 'Gambia', 3),
    ('GEO', 'Georgia', 3),
    ('DEU', 'Germany', 5),
    ('GHA', 'Ghana', 3),
    ('GIB', 'Gibraltar', 1),
    ('GRC', 'Greece', 4),
    ('GRL', 'Greenland', 2),
    ('GRD', 'Grenada', 2),
    ('GLP', 'Guadeloupe', 3),
    ('GUM', 'Guam', 2),
    ('GTM', 'Guatemala', 3),
    ('GGY', 'Guernsey', 2),
    ('GIN', 'Guinea', 4),
    ('GNB', 'Guinea-Bissau', 3),
    ('GUY', 'Guyana', 3),
    ('HTI', 'Haiti', 5),
    ('HMD', 'Heard Island and McDonald Islands', 1),
    ('HND', 'Honduras', 3),
    ('HKG', 'Hong Kong', 2),
    ('HUN', 'Hungary', 3),
    ('ISL', 'Iceland', 3),
    ('IND', 'India', 4),
    ('IDN', 'Indonesia', 5),
    ('IRN', 'Iran', 3),
    ('IRQ', 'Iraq', 3),
    ('IRL', 'Ireland', 2),
    ('IMN', 'Isle of Man', 3),
    ('ISR', 'Israel', 2),
    ('ITA', 'Italy', 4),
    ('JAM', 'Jamaica', 2),
    ('JPN', 'Japan', 3),
    ('JEY', 'Jersey', 2),
    ('JOR', 'Jordan', 3),
    ('KAZ', 'Kazakhstan', 3),
    ('KEN', 'Kenya', 4),
    ('KIR', 'Kiribati', 1),
    ('XKO', 'Kosovo', 3),
    ('KWT', 'Kuwait', 2),
    ('KGZ', 'Kyrgyzstan', 3),
    ('LAO', 'Laos', 3),
    ('LVA', 'Latvia', 3),
    ('LBN', 'Lebanon', 4),
    ('LSO', 'Lesotho', 2),
    ('LBR', 'Liberia', 4),
    ('LBY', 'Libya', 2),
    ('LIE', 'Liechtenstein', 2),
    ('LTU', 'Lithuania', 3),
    ('LUX', 'Luxembourg', 5),
    ('MAC', 'Macao', 3),
    ('MKD', 'Macedonia', 2),
    ('MDG', 'Madagascar', 5),
    ('MWI', 'Malawi', 4),
    ('MYS', 'Malaysia', 3),
    ('MDV', 'Maldives', 1),
    ('MLI', 'Mali', 5),
    ('MLT', 'Malta', 3),
    ('MHL', 'Marshall Islands', 1),
    ('MTQ', 'Martinique', 3),
    ('MRT', 'Mauritania', 3),
    ('MUS', 'Mauritius', 2),
    ('MYT', 'Mayotte', 2),
    ('MEX', 'Mexico', 3),
    ('FSM', 'Micronesia', 2),
    ('MDA', 'Moldova', 2),
    ('MCO', 'Monaco', 1),
    ('MNG', 'Mongolia', 3),
    ('MNE', 'Montenegro', 2),
    ('MSR', 'Montserrat', 2),
    ('MAR', 'Morocco', 5),
    ('MOZ', 'Mozambique', 4),
    ('MMR', 'Myanmar', 4),
    ('NAM', 'Namibia', 3),
    ('NRU', 'Nauru', 2),
    ('NPL', 'Nepal', 5),
    ('NLD', 'Netherlands', 3),
    ('NCL', 'New Caledonia', 3),
    ('NZL', 'New Zealand', 3),
    ('NIC', 'Nicaragua', 3),
    ('NER', 'Niger', 4),
    ('NGA', 'Nigeria', 3),
    ('NIU', 'Niue', 1),
    ('NFK', 'Norfolk Island', 1),
    ('PRK', 'North Korea', 3),
    ('XNC', 'Northern Cyprus', 2),
    ('MNP', 'Northern Mariana Islands', 2),
    ('NOR', 'Norway', 3),
    ('OMN', 'Oman', 3),
    ('PAK', 'Pakistan', 4),
    ('PLW', 'Palau', 2),
    ('PSE', 'Palestina', 3),
    ('PAN', 'Panama', 4),
    ('PNG', 'Papua New Guinea', 3),
    ('XPI', 'Paracel Islands', 1),
    ('PRY', 'Paraguay', 3),
    ('PER', 'Peru', 4),
    ('PHL', 'Philippines', 4),
    ('PCN', 'Pitcairn Islands', 1),
    ('POL', 'Poland', 4),
    ('PRT', 'Portugal', 4),
    ('PRI', 'Puerto Rico', 2),
    ('QAT', 'Qatar', 2),
    ('COG', 'Republic of Congo', 3),
    ('REU', 'Reunion', 3),
    ('ROU', 'Romania', 3),
    ('RUS', 'Russia', 4),
    ('RWA', 'Rwanda', 6),
    ('BLM', 'Saint-BarthÃ©lemy', 1),
    ('MAF', 'Saint-Martin', 1),
    ('SHN', 'Saint Helena', 3),
    ('KNA', 'Saint Kitts and Nevis', 2),
    ('LCA', 'Saint Lucia', 2),
    ('SPM', 'Saint Pierre and Miquelon', 2),
    ('VCT', 'Saint Vincent and the Grenadines', 2),
    ('WSM', 'Samoa', 3),
    ('SMR', 'San Marino', 2),
    ('STP', 'Sao Tome and Principe', 3),
    ('SAU', 'Saudi Arabia', 2),
    ('SEN', 'Senegal', 5),
    ('SRB', 'Serbia', 3),
    ('SYC', 'Seychelles', 2),
    ('SLE', 'Sierra Leone', 4),
    ('SGP', 'Singapore', 2),
    ('SXM', 'Sint Maarten', 1),
    ('SVK', 'Slovakia', 3),
    ('SVN', 'Slovenia', 3),
    ('SLB', 'Solomon Islands', 3),
    ('SOM', 'Somalia', 3),
    ('ZAF', 'South Africa', 5),
    ('SGS', 'South Georgia and the South Sandwich Islands', 1),
    ('KOR', 'South Korea', 3),
    ('SSD', 'South Sudan', 4),
    ('ESP', 'Spain', 5),
    ('XSP', 'Spratly islands', 1),
    ('LKA', 'Sri Lanka', 3),
    ('SDN', 'Sudan', 4),
    ('SUR', 'Suriname', 3),
    ('SJM', 'Svalbard and Jan Mayen', 2),
    ('SWZ', 'Swaziland', 3),
    ('SWE', 'Sweden', 3),
    ('CHE', 'Switzerland', 4),
    ('SYR', 'Syria', 3),
    ('TWN', 'Taiwan', 3),
    ('TJK', 'Tajikistan', 4),
    ('TZA', 'Tanzania', 4),
    ('THA', 'Thailand', 4),
    ('TGO', 'Togo', 3),
    ('TKL', 'Tokelau', 2),
    ('TON', 'Tonga', 2),
    ('TTO', 'Trinidad and Tobago', 2),
    ('TUN', 'Tunisia', 3),
    ('TUR', 'Turkey', 3),
    ('TKM', 'Turkmenistan', 2),
    ('TCA', 'Turks and Caicos Islands', 2),
    ('TUV', 'Tuvalu', 2),
    ('UGA', 'Uganda', 5),
    ('UKR', 'Ukraine', 3),
    ('ARE', 'United Arab Emirates', 4),
    ('GBR', 'United Kingdom', 4),
    ('USA', 'United States', 3),
    ('UMI', 'United States Minor Outlying Islands', 2),
    ('URY', 'Uruguay', 3),
    ('UZB', 'Uzbekistan', 3),
    ('VUT', 'Vanuatu', 3),
    ('VAT', 'Vatican City', 1),
    ('VEN', 'Venezuela', 3),
    ('VNM', 'Vietnam', 4),
    ('VIR', 'Virgin Islands, U.S.', 3),
    ('WLF', 'Wallis and Futuna', 3),
    ('ESH', 'Western Sahara', 2),
    ('YEM', 'Yemen', 3),
    ('ZMB', 'Zambia', 3),
    ('ZWE', 'Zimbabwe', 3)]

SHP_FILE_DIR = "zip://C:/Users/spiro.huang/workspace/gadm/shps"
DATA_URL_TEMP = SHP_FILE_DIR + "/gadm36_{country_code}_shp.zip!gadm36_{country_code}_{level}.shp"

class Country:
    def __init__(self, country_code, nums_of_level):
        self.country_code = country_code
        self.gid = country_code
        self.nums_of_level = nums_of_level
        self.name = None
        self.geometry = None
        self.subDivisions = {} # key: level1-gid value: level1 Division object


class Division:
    def __init__(self, gid, name, varname, nl_name, hasc, type, engtype):
        self.gid = gid
        self.name = name
        self.varname = varname
        self.nl_name = nl_name
        self.hasc = hasc
        self.type = type
        self.engtype = engtype




class LocationParser:
    def __init__(self, shp_file_dir):
        self.data_url_temp = shp_file_dir + "/gadm36_{country_code}_shp.zip!gadm36_{country_code}_{level}.shp"
        self.level0 = []  # List<class 'pandas.core.series.Series'>
        self.level1 = {}  # key level0 GID, value: List of level1 <class 'pandas.core.series.Series'>
        self.level2 = {}  # key level1 GID, value: List of level2 <class 'pandas.core.series.Series'>

    def load(self):
        for country in ALL_COUNTRIES:
            country_code = country[0]
            nums_of_level = country[2]

            for level in range(nums_of_level):
                if level > 2:
                    # Only supports 3 levels at most
                    break
                data_url = self.data_url_temp.format(country_code=country_code, level=level)
                df = geopandas.read_file(data_url)

                if level == 0:
                    for index, row in df.iterrows():
                        self.level0.append(row)

                if level == 1:

                    for index, row in df.iterrows():
                        gid = row['GID_1']
                        parent_gid = gid[0:gid.rindex(".")]
                        self.level1[parent_gid]











