import { useState } from 'react'
import { supabase } from '../lib/supabase'
import { X, ChevronDown, ChevronUp } from 'lucide-react'
import { STAGES, PROPERTY_TYPES } from '../lib/constants'

const FINANCE_PURPOSES = ['Acquisition','Refinance','Construction','Bridge','Mezzanine','Preferred Equity','Recapitalization','Other']
const CAPITAL_TYPES = ['Debt','Equity','Preferred Equity','Mezzanine']
const DEBT_EQUITY_TYPES = ['Permanent','Bridge','Construction','Mini-Perm','CMBS','Agency','SBA','Life Company','Bank','Credit Union','Debt Fund','Other']
const FEE_TYPES = ['Percentage','Flat Fee']
const RATE_TYPES = ['Fixed','Floating','Fixed to Floating']
const RATE_INDEXES = ['SOFR','Prime','Treasury','LIBOR','Other']
const RECOURSE_TYPES = ['Full Recourse','Non-Recourse','Partial Recourse','Carve-Out Guaranty']
const FEE_AGREEMENT_TYPES = ['Exclusive','Non-Exclusive','Right of First Refusal']

const EMPTY = {
  borrower_name:'',stage:'Prospecting',expected_close_date:'',
  property_address:'',city:'',state_province:'',zip_code:'',
  property_type:'',total_units:'',sq_ft:'',year_built:'',
  loan_amount:'',finance_purpose:'',capital_type:'Debt',debt_equity_type:'',
  lender_name:'',term_months:'',amortization_months:'',io_months:'',
  interest_rate_type:'',interest_rate_index:'',base_rate:'',spread_bps:'',
  interest_rate:'',ltv:'',dscr:'',recourse:'',
  maturity_date:'',prepay_penalty_exp:'',prepay_description:'',capital_notes:'',
  capital_exit_fee_pct:'',capital_exit_fee_amt:'',
  origination_fee_type:'Percentage',origination_fee_pct:'',
  origination_fee_amt:'',commission_fee:'',
  fee_agreement_type:'Exclusive',engagement_date:'',
  term_sheet_date:'',rate_lock_date:'',x1031_exchange:false,
  referral_source:'',referred_by:'',referral_notes:'',notes:'',
}

const IS = {width:'100%',background:'var(--surface2)',border:'1px solid var(--border)',color:'var(--text)',borderRadius:'6px',padding:'7px 10px',fontSize:'12px',fontFamily:'DM Sans, sans-serif',transition:'border-color 0.15s',boxSizing:'border-box'}
const LS = {display:'block',marginBottom:'4px',fontSize:'10px',fontWeight:700,color:'var(--muted)',fontFamily:'Syne, sans-serif',textTransform:'uppercase',letterSpacing:'0.08em'}

function F({label,children,span}){return <div style={{gridColumn:span===2?'1 / -1':span===3?'1 / -1':'auto'}}><label style={LS}>{label}</label>{children}</div>}
function Sel({value,onChange,options}){return <select value={value} onChange={onChange} style={IS}><option value="">Select...</option>{options.map(o=><option key={o} value={o}>{o}</option>)}</select>}
function Inp({type='text',value,onChange,placeholder,step}){return <input type={type} value={value} onChange={onChange} placeholder={placeholder} step={step} style={IS}/>}

function Section({title,children,defaultOpen=true}){
  const [open,setOpen]=useState(defaultOpen)
  return(
    <div style={{marginBottom:'4px'}}>
      <button type="button" onClick={()=>setOpen(o=>!o)} style={{width:'100%',display:'flex',alignItems:'center',justifyContent:'space-between',background:'var(--surface2)',border:'1px solid var(--border)',color:'var(--text)',padding:'7px 12px',borderRadius:'6px',cursor:'pointer',fontFamily:'Syne, sans-serif',fontWeight:700,fontSize:'11px',letterSpacing:'0.06em',textTransform:'uppercase',marginBottom:open?'12px':'0'}}>
        {title}{open?<ChevronUp size={13}/>:<ChevronDown size={13}/>}
      </button>
      {open&&<div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:'10px 14px',paddingBottom:'14px'}}>{children}</div>}
    </div>
  )
}

export default function DealModal({deal,session,onClose,onSaved}){
  const [form,setForm]=useState(()=>{
    if(!deal)return{...EMPTY}
    const f={...EMPTY,...deal}
    Object.keys(f).forEach(k=>{if(f[k]===null||f[k]===undefined)f[k]=''})
    f.x1031_exchange=!!deal.x1031_exchange
    return f
  })
  const [saving,setSaving]=useState(false)
  const [error,setError]=useState('')

  function set(k,v){setForm(f=>({...f,[k]:v}))}
  function num(v){return v!==''?parseFloat(v):null}
  function int(v){return v!==''?parseInt(v):null}
  function str(v){return v?.trim()||null}
  function dt(v){return v||null}

  async function handleSave(){
    if(!form.borrower_name.trim()){setError('Borrower name is required.');return}
    setSaving(true);setError('')
    const p={
      borrower_name:str(form.borrower_name),stage:form.stage,expected_close_date:dt(form.expected_close_date),
      property_address:str(form.property_address),city:str(form.city),state_province:str(form.state_province),zip_code:str(form.zip_code),
      property_type:str(form.property_type),total_units:int(form.total_units),sq_ft:num(form.sq_ft),year_built:int(form.year_built),
      loan_amount:num(form.loan_amount),finance_purpose:str(form.finance_purpose),capital_type:str(form.capital_type),debt_equity_type:str(form.debt_equity_type),
      lender_name:str(form.lender_name),term_months:int(form.term_months),amortization_months:int(form.amortization_months),io_months:int(form.io_months),
      interest_rate_type:str(form.interest_rate_type),interest_rate_index:str(form.interest_rate_index),
      base_rate:num(form.base_rate),spread_bps:int(form.spread_bps),interest_rate:num(form.interest_rate),
      ltv:num(form.ltv),dscr:num(form.dscr),recourse:str(form.recourse),
      maturity_date:dt(form.maturity_date),prepay_penalty_exp:dt(form.prepay_penalty_exp),
      prepay_description:str(form.prepay_description),capital_notes:str(form.capital_notes),
      capital_exit_fee_pct:num(form.capital_exit_fee_pct),capital_exit_fee_amt:num(form.capital_exit_fee_amt),
      origination_fee_type:str(form.origination_fee_type),origination_fee_pct:num(form.origination_fee_pct),
      origination_fee_amt:num(form.origination_fee_amt),commission_fee:num(form.commission_fee),
      fee_agreement_type:str(form.fee_agreement_type),engagement_date:dt(form.engagement_date),
      term_sheet_date:dt(form.term_sheet_date),rate_lock_date:dt(form.rate_lock_date),x1031_exchange:!!form.x1031_exchange,
      referral_source:str(form.referral_source),referred_by:str(form.referred_by),referral_notes:str(form.referral_notes),
      notes:str(form.notes),updated_at:new Date().toISOString(),
    }
    let err
    if(deal?.id){;({error:err}=await supabase.from('deals').update(p).eq('id',deal.id))}
    else{;({error:err}=await supabase.from('deals').insert({...p,created_by:session.user.id}))}
    if(err){setError(err.message);setSaving(false);return}
    onSaved();onClose()
  }

  return(
    <div onClick={e=>{if(e.target===e.currentTarget)onClose()}} style={{position:'fixed',inset:0,zIndex:1000,background:'rgba(0,0,0,0.8)',backdropFilter:'blur(6px)',display:'flex',alignItems:'center',justifyContent:'center',padding:'16px'}}>
      <div style={{background:'var(--surface)',border:'1px solid var(--border)',borderRadius:'12px',width:'100%',maxWidth:'860px',maxHeight:'94vh',display:'flex',flexDirection:'column',boxShadow:'0 32px 80px rgba(0,0,0,0.7)'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'16px 22px',borderBottom:'1px solid var(--border)',flexShrink:0}}>
          <div>
            <h2 style={{fontFamily:'Syne, sans-serif',fontWeight:700,fontSize:'16px',color:'var(--text)',marginBottom:'1px'}}>{deal?'Edit Deal':'New Deal'}</h2>
            {deal&&<div style={{fontSize:'11px',color:'var(--muted)',fontFamily:'IBM Plex Mono, monospace'}}>{deal.borrower_name}</div>}
          </div>
          <button onClick={onClose} style={{background:'transparent',border:'1px solid var(--border)',color:'var(--muted)',cursor:'pointer',padding:'5px',borderRadius:'6px',display:'flex',alignItems:'center'}}><X size={15}/></button>
        </div>
        <div style={{overflowY:'auto',flex:1,padding:'16px 22px',display:'flex',flexDirection:'column',gap:'4px'}}>
          <Section title="Summary">
            <F label="Borrower / Client *"><Inp value={form.borrower_name} onChange={e=>set('borrower_name',e.target.value)} placeholder="Larry Li"/></F>
            <F label="Stage"><Sel value={form.stage} onChange={e=>set('stage',e.target.value)} options={STAGES}/></F>
            <F label="Close Date"><Inp type="date" value={form.expected_close_date} onChange={e=>set('expected_close_date',e.target.value)}/></F>
            <F label="Proceeds / Loan Amount ($)"><Inp type="number" value={form.loan_amount} onChange={e=>set('loan_amount',e.target.value)} placeholder="27500000"/></F>
            <F label="Finance Purpose"><Sel value={form.finance_purpose} onChange={e=>set('finance_purpose',e.target.value)} options={FINANCE_PURPOSES}/></F>
            <F label="Capital Type"><Sel value={form.capital_type} onChange={e=>set('capital_type',e.target.value)} options={CAPITAL_TYPES}/></F>
            <F label="Debt / Equity Type"><Sel value={form.debt_equity_type} onChange={e=>set('debt_equity_type',e.target.value)} options={DEBT_EQUITY_TYPES}/></F>
            <F label="Fee Agreement Type"><Sel value={form.fee_agreement_type} onChange={e=>set('fee_agreement_type',e.target.value)} options={FEE_AGREEMENT_TYPES}/></F>
            <F label="1031 Exchange"><div style={{display:'flex',alignItems:'center',gap:'8px',paddingTop:'6px'}}><input type="checkbox" checked={!!form.x1031_exchange} onChange={e=>set('x1031_exchange',e.target.checked)} style={{width:'14px',height:'14px',accentColor:'var(--gold)',cursor:'pointer'}}/><span style={{fontSize:'12px',color:'var(--muted)'}}>Yes</span></div></F>
          </Section>
          <Section title="Property Details">
            <F label="Property Type"><Sel value={form.property_type} onChange={e=>set('property_type',e.target.value)} options={PROPERTY_TYPES}/></F>
            <F label="Address" span={2}><Inp value={form.property_address} onChange={e=>set('property_address',e.target.value)} placeholder="111 San Bruno Ave W"/></F>
            <F label="City"><Inp value={form.city} onChange={e=>set('city',e.target.value)} placeholder="San Bruno"/></F>
            <F label="State / Province"><Inp value={form.state_province} onChange={e=>set('state_province',e.target.value)} placeholder="California"/></F>
            <F label="Zip / Postal Code"><Inp value={form.zip_code} onChange={e=>set('zip_code',e.target.value)} placeholder="94066"/></F>
            <F label="Total Units"><Inp type="number" value={form.total_units} onChange={e=>set('total_units',e.target.value)} placeholder="46"/></F>
            <F label="Property Size (Sq Ft)"><Inp type="number" value={form.sq_ft} onChange={e=>set('sq_ft',e.target.value)} placeholder="111400"/></F>
            <F label="Year Built"><Inp type="number" value={form.year_built} onChange={e=>set('year_built',e.target.value)} placeholder="2020"/></F>
          </Section>
          <Section title="Capital Details">
            <F label="Capital Source (Lender)"><Inp value={form.lender_name} onChange={e=>set('lender_name',e.target.value)} placeholder="East West Bank"/></F>
            <F label="Term (Months)"><Inp type="number" value={form.term_months} onChange={e=>set('term_months',e.target.value)} placeholder="360"/></F>
            <F label="Amortization (Months)"><Inp type="number" value={form.amortization_months} onChange={e=>set('amortization_months',e.target.value)} placeholder="360"/></F>
            <F label="I/O (Months)"><Inp type="number" value={form.io_months} onChange={e=>set('io_months',e.target.value)} placeholder="24"/></F>
            <F label="Interest Rate Type"><Sel value={form.interest_rate_type} onChange={e=>set('interest_rate_type',e.target.value)} options={RATE_TYPES}/></F>
            <F label="Interest Rate Index"><Sel value={form.interest_rate_index} onChange={e=>set('interest_rate_index',e.target.value)} options={RATE_INDEXES}/></F>
            <F label="Base Rate (%)"><Inp type="number" value={form.base_rate} onChange={e=>set('base_rate',e.target.value)} placeholder="5.25" step="0.01"/></F>
            <F label="Spread (bps)"><Inp type="number" value={form.spread_bps} onChange={e=>set('spread_bps',e.target.value)} placeholder="250"/></F>
            <F label="Interest Rate (%)"><Inp type="number" value={form.interest_rate} onChange={e=>set('interest_rate',e.target.value)} placeholder="6.50" step="0.01"/></F>
            <F label="LTV/LTC (%)"><Inp type="number" value={form.ltv} onChange={e=>set('ltv',e.target.value)} placeholder="65" step="0.1"/></F>
            <F label="DSCR"><Inp type="number" value={form.dscr} onChange={e=>set('dscr',e.target.value)} placeholder="1.25" step="0.01"/></F>
            <F label="Recourse"><Sel value={form.recourse} onChange={e=>set('recourse',e.target.value)} options={RECOURSE_TYPES}/></F>
            <F label="Maturity Date"><Inp type="date" value={form.maturity_date} onChange={e=>set('maturity_date',e.target.value)}/></F>
            <F label="Prepay Penalty Exp Date"><Inp type="date" value={form.prepay_penalty_exp} onChange={e=>set('prepay_penalty_exp',e.target.value)}/></F>
            <F label="Prepay Description"><Inp value={form.prepay_description} onChange={e=>set('prepay_description',e.target.value)} placeholder="5-4-3-2-1 step-down"/></F>
            <F label="Capital Exit Fee (%)"><Inp type="number" value={form.capital_exit_fee_pct} onChange={e=>set('capital_exit_fee_pct',e.target.value)} placeholder="1.00" step="0.01"/></F>
            <F label="Capital Exit Fee ($)"><Inp type="number" value={form.capital_exit_fee_amt} onChange={e=>set('capital_exit_fee_amt',e.target.value)} placeholder="275000"/></F>
            <F label="Capital Notes" span={3}><textarea value={form.capital_notes} onChange={e=>set('capital_notes',e.target.value)} rows={2} placeholder="Lender-specific notes..." style={{...IS,resize:'vertical',lineHeight:1.5}}/></F>
          </Section>
          <Section title="Fee Details">
            <F label="Origination Fee Type"><Sel value={form.origination_fee_type} onChange={e=>set('origination_fee_type',e.target.value)} options={FEE_TYPES}/></F>
            <F label="Origination Fee (%)"><Inp type="number" value={form.origination_fee_pct} onChange={e=>set('origination_fee_pct',e.target.value)} placeholder="1.000" step="0.001"/></F>
            <F label="Origination Fee ($)"><Inp type="number" value={form.origination_fee_amt} onChange={e=>set('origination_fee_amt',e.target.value)} placeholder="275000"/></F>
            <F label="Total Commission / Fee ($)"><Inp type="number" value={form.commission_fee} onChange={e=>set('commission_fee',e.target.value)} placeholder="275000"/></F>
            <F label="Engagement Executed Date"><Inp type="date" value={form.engagement_date} onChange={e=>set('engagement_date',e.target.value)}/></F>
            <F label="Term Sheet / LOI Date"><Inp type="date" value={form.term_sheet_date} onChange={e=>set('term_sheet_date',e.target.value)}/></F>
            <F label="Rate Lock Date"><Inp type="date" value={form.rate_lock_date} onChange={e=>set('rate_lock_date',e.target.value)}/></F>
          </Section>
          <Section title="Referral Details" defaultOpen={false}>
            <F label="Referral Source"><Inp value={form.referral_source} onChange={e=>set('referral_source',e.target.value)} placeholder="John Smith"/></F>
            <F label="Referred By"><Inp value={form.referred_by} onChange={e=>set('referred_by',e.target.value)} placeholder="Internal or external"/></F>
            <F label="Referral Notes" span={3}><textarea value={form.referral_notes} onChange={e=>set('referral_notes',e.target.value)} rows={2} placeholder="Referral context..." style={{...IS,resize:'vertical',lineHeight:1.5}}/></F>
          </Section>
          <Section title="General Notes" defaultOpen={false}>
            <F label="Notes / Next Steps" span={3}><textarea value={form.notes} onChange={e=>set('notes',e.target.value)} rows={3} placeholder="Key next steps, outstanding items..." style={{...IS,resize:'vertical',lineHeight:1.5}}/></F>
          </Section>
          {error&&<div style={{padding:'10px 14px',borderRadius:'6px',background:'rgba(248,81,73,0.08)',border:'1px solid rgba(248,81,73,0.25)',color:'var(--danger)',fontSize:'13px'}}>{error}</div>}
        </div>
        <div style={{padding:'12px 22px',borderTop:'1px solid var(--border)',display:'flex',justifyContent:'flex-end',gap:'10px',flexShrink:0}}>
          <button onClick={onClose} style={{background:'transparent',border:'1px solid var(--border)',color:'var(--text)',padding:'8px 20px',borderRadius:'6px',cursor:'pointer',fontFamily:'Syne, sans-serif',fontWeight:600,fontSize:'12px',letterSpacing:'0.04em'}}>CANCEL</button>
          <button onClick={handleSave} disabled={saving} style={{background:saving?'var(--gold-dim)':'var(--gold)',border:'none',color:'#000',padding:'8px 24px',borderRadius:'6px',cursor:saving?'not-allowed':'pointer',fontFamily:'Syne, sans-serif',fontWeight:700,fontSize:'12px',letterSpacing:'0.04em'}}>{saving?'SAVING...':deal?'SAVE CHANGES':'ADD DEAL'}</button>
        </div>
      </div>
    </div>
  )
}
