import maya.cmds as cmds
import maya.api.OpenMaya as om

# Add function that indicates to maya to use api 2.0
def maya_useNewAPI():
    pass

# Create my evaluate pyton function
class python_execute(om.MPxNode):

    # TYPE_NAME is the name you use when looking up nodes in the Node Editor.
    TYPE_NAME = "pyExecute"

    # The TYPE_ID is used to tell maya how to save your plugin in binary files.
    # 0x0007F7F7 is a development id. You can itterate it and use 0x0007F7F8, 0x0007F7F9, etc.
    TYPE_ID = om.MTypeId(0x0007F7F7)

    # Here I define all of my obj variables.
    # They need to be objs since I store an instance of a class that defines a data type. (Done in initialize)
    py_code_obj = None

    variable_a_obj = None
    variable_b_obj = None
    variable_c_obj = None
    variable_d_obj = None

    output_obj = None

    # init is used to initialize all variables associated with the parent class.
    def __init__(self):
        super(python_execute, self).__init__()
    
    # This function is called when a plug is "dirty". Aka. when the node needs to be updated its outputs get recomputed.
    def compute(self, plug, data):
        if plug != python_execute.output_obj:
            return

        # Use a try: except: block to return custom errors and prevent crashes.
        try:
            # Get inputs from the objs that store them.
            py_code = data.inputValue(python_execute.py_code_obj).asString()
            a = data.inputValue(python_execute.variable_a_obj).asFloat()
            b = data.inputValue(python_execute.variable_b_obj).asFloat()
            c = data.inputValue(python_execute.variable_c_obj).asFloat()
            d = data.inputValue(python_execute.variable_d_obj).asFloat()

            # Exec the string code with the python exec function
            local_vars = {"a": a, "b": b, "c": c, "d": d, "output": 0.0}
            exec(py_code, {}, local_vars)

            # Return 0.0 if output was not defined or the new value if it was define.
            # NB| Output needs to be defined in the users code in order for this to work properly
            # Example: output = a + b
            result = local_vars.get("output", 0.0)
            data.outputValue(python_execute.output_obj).setFloat(result)

        except Exception as e:
            om.MGlobal.displayError(f"[pyEvaluate] Error: {str(e)}")
            data.outputValue(python_execute.output_obj).setFloat(0.0)

        data.setClean(plug)

    # Why classmethod here? Well there is not object yet so using self to reffer to the class wouldn't work. Therefore a @classmethod is used.
    # cls reffers to the class -> python_execute in this case

    # Create an instance of the class.
    @classmethod
    def creator(cls):
        return python_execute()
    
    # Initialize the variables associated with the class.
    @classmethod
    def initialize(cls):
        # Here I set the function sets ("MFn") instances so that the code is easier to read.
        typed_attr = om.MFnTypedAttribute()
        numeric_attr = om.MFnNumericAttribute()

        # Create a default string data object
        default_string = om.MFnStringData().create("")

        # pyCode attribute (string)
        cls.py_code_obj = typed_attr.create("pyCode", "pyC", om.MFnData.kString, default_string)
        om.MFnAttribute(cls.py_code_obj).writable = True
        om.MFnAttribute(cls.py_code_obj).storable = True
        om.MFnAttribute(cls.py_code_obj).readable = True

        # Float inputs
        cls.variable_a_obj = numeric_attr.create("variable_a", "var_a", om.MFnNumericData.kFloat, 0.0)
        om.MFnAttribute(cls.variable_a_obj).keyable = True
        cls.variable_b_obj = numeric_attr.create("variable_b", "var_b", om.MFnNumericData.kFloat, 0.0)
        om.MFnAttribute(cls.variable_b_obj).keyable = True
        cls.variable_c_obj = numeric_attr.create("variable_c", "var_c", om.MFnNumericData.kFloat, 0.0)
        om.MFnAttribute(cls.variable_c_obj).keyable = True
        cls.variable_d_obj = numeric_attr.create("variable_d", "var_d", om.MFnNumericData.kFloat, 0.0)
        om.MFnAttribute(cls.variable_d_obj).keyable = True

        # Output
        cls.output_obj = numeric_attr.create("output", "otp", om.MFnNumericData.kFloat, 0.0)
        om.MFnAttribute(cls.output_obj).writable = False
        om.MFnAttribute(cls.output_obj).storable = False

        # Add attributes
        cls.addAttribute(cls.py_code_obj)
        cls.addAttribute(cls.variable_a_obj)
        cls.addAttribute(cls.variable_b_obj)
        cls.addAttribute(cls.variable_c_obj)
        cls.addAttribute(cls.variable_d_obj)
        cls.addAttribute(cls.output_obj)

        # Set which attributes affect which attributes. Very important for correct updating.
        # In this case all attributes can change and if they do they should change the output value.
        cls.attributeAffects(cls.py_code_obj, cls.output_obj)
        cls.attributeAffects(cls.variable_a_obj, cls.output_obj)
        cls.attributeAffects(cls.variable_b_obj, cls.output_obj)
        cls.attributeAffects(cls.variable_c_obj, cls.output_obj)
        cls.attributeAffects(cls.variable_d_obj, cls.output_obj)


# Runs when load plugin is called
def initializePlugin(plugin):
    # Define mandatory information for your plugin.
    vendor = "EV"
    version = "1.0.0"

    # Here I set the function sets ("MFn") instances so that the code is easier to read.
    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    # Use a try: except: block to return custom errors and prevent crashes.
    try:
        plugin_fn.registerNode(
            python_execute.TYPE_NAME,
            python_execute.TYPE_ID,
            python_execute.creator,
            python_execute.initialize,
            om.MPxNode.kDependNode
        )
        om.MGlobal.displayInfo(f"Registered node: {python_execute.TYPE_NAME}")

    except Exception as e:
        om.MGlobal.displayError(f"Failed to register node: {python_execute.TYPE_NAME} | {str(e)}")

# Runs when unload plugin is called
def uninitializePlugin(plugin):

    # Here I set the function sets ("MFn") instances so that the code is easier to read.
    plugin_fn = om.MFnPlugin(plugin)

    # Use a try: except: block to return custom errors and prevent crashes.
    try:
        plugin_fn.deregisterNode(python_execute.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node: {0}".format(python_execute.TYPE_NAME))

# This runs only if the file that is being executed is this file. This section is used for debugging and quicker development.
if __name__ == "__main__":

    plugin_name = "python_execute.py"

    # ecalDeferred executes code in the form of a string only after Maya has finished loading.

    # Load and Unload the plugin.
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name)) # Uncomment if necessary.
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

    # Create a test.
    cmds.evalDeferred('cmds.createNode("pyExecute")')